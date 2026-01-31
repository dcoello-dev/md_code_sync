from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class JobStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    AWAITING_PARTS = "awaiting_parts"
    COMPLETED = "completed"
    DELIVERED = "delivered"

class Person(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    phone: Optional[str] = None

class Client(Person):
    client_id: str
    vip_status: bool = False

class Employee(Person):
    employee_id: str
    role: str
    specialization: Optional[str] = None

class Vehicle(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17)
    plate: str
    make: str
    model: str
    year: int
    owner: Client

class Part(BaseModel):
    sku: str
    name: str
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)

class RepairJob(BaseModel):
    job_id: str
    vehicle: Vehicle
    mechanic: Employee
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    parts_used: List[Part] = []
    description: str
    total_cost: float = 0.0

    def calculate_total(self, labor_rate: float = 50.0, hours: float = 0.0) -> float:
        parts_cost = sum(part.price for part in self.parts_used)
        self.total_cost = parts_cost + (labor_rate * hours)
        return self.total_cost

def get_mock_workshop_data(num_clients: int = 20, num_jobs: int = 50) -> List[RepairJob]:
    """Generates a large set of mock workshop data."""
    try:
        from faker import Faker
    except ImportError:
        # Fallback if faker is not available (though we just installed it)
        return []

    fake = Faker()
    
    # 1. Create employees
    employees = [
        Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.company_email(),
            employee_id=f"EMP-{i:03d}",
            role=fake.job(),
            specialization=fake.random_element(["Engines", "Brakes", "Electronics", "Bodywork", "Tires"])
        ) for i in range(5)
    ]

    # 2. Create clients and their vehicles
    clients = []
    vehicles = []
    for i in range(num_clients):
        client = Client(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            client_id=f"CLI-{i:03d}",
            vip_status=fake.boolean(chance_of_getting_true=20)
        )
        clients.append(client)
        
        # Each client has 1-2 vehicles
        for j in range(fake.random_int(1, 2)):
            vehicles.append(Vehicle(
                vin=fake.unique.bothify(text='?'*17).upper(),
                plate=fake.license_plate(),
                make=fake.random_element(["Toyota", "Ford", "VW", "BMW", "Audi", "Fiat"]),
                model=fake.word().capitalize(),
                year=fake.year(),
                owner=client
            ))

    # 3. Create common parts
    all_parts = [
        Part(sku=fake.unique.bothify(text='??-####').upper(), name=fake.word().capitalize(), price=fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=5.0), stock_quantity=fake.random_int(0, 50))
        for _ in range(30)
    ]

    # 4. Create repair jobs
    jobs = []
    for i in range(num_jobs):
        vehicle = fake.random_element(vehicles)
        mechanic = fake.random_element(employees)
        status = fake.random_element(list(JobStatus))
        
        # Sub-selection of parts for this job
        parts_used = fake.random_elements(elements=all_parts, length=fake.random_int(1, 5), unique=True)
        
        job = RepairJob(
            job_id=f"JOB-{fake.year()}-{i:04d}",
            vehicle=vehicle,
            mechanic=mechanic,
            status=status,
            created_at=fake.date_time_this_year(),
            description=fake.sentence(nb_words=10),
            parts_used=parts_used
        )
        
        # Calculate final cost if completed
        if status == JobStatus.COMPLETED or status == JobStatus.DELIVERED:
            job.completed_at = datetime.now()
            job.calculate_total(hours=fake.random_int(1, 8))
        
        jobs.append(job)

    return jobs
