from universalviewer.domain.workshop import Client, Employee, Vehicle, Part, RepairJob, JobStatus
from pprint import pprint

def verify():
    print("--- Verificando Modelos de Dominio (Taller) ---")
    
    # 1. Crear un Cliente
    client = Client(
        first_name="Juan",
        last_name="Pérez",
        email="juan.perez@example.com",
        client_id="CLI-001",
        vip_status=True
    )
    print(f"Cliente creado: {client.first_name} {client.last_name} (VIP: {client.vip_status})")

    # 2. Crear un Vehículo asociado al cliente
    vehicle = Vehicle(
        vin="1234567890ABCDEFG", # 17 caracteres
        plate="1234-ABC",
        make="Toyota",
        model="Corolla",
        year=2022,
        owner=client
    )
    print(f"Vehículo creado: {vehicle.make} {vehicle.model} de {vehicle.owner.first_name}")

    # 3. Crear un Empleado (Mecánico)
    mechanic = Employee(
        first_name="Carlos",
        last_name="García",
        email="carlos.mechanic@workshop.com",
        employee_id="EMP-42",
        role="Senior Mechanic",
        specialization="Hybrid Engines"
    )

    # 4. Crear piezas
    oil_filter = Part(sku="OIL-001", name="Filtro de Aceite", price=15.50, stock_quantity=10)
    synthetic_oil = Part(sku="LUB-099", name="Aceite Sintético 5W30", price=45.00, stock_quantity=5)

    # 5. Crear una Orden de Reparación
    job = RepairJob(
        job_id="JOB-2026-001",
        vehicle=vehicle,
        mechanic=mechanic,
        description="Cambio de aceite y revisión general",
        parts_used=[oil_filter, synthetic_oil]
    )
    
    # 6. Calcular total
    total = job.calculate_total(hours=1.5)
    print(f"Orden de Trabajo {job.job_id} creada.")
    print(f"Mecánico asignado: {job.mechanic.first_name} ({job.mechanic.specialization})")
    print(f"Costo Total Estimado: {total:.2f}€")
    print(f"Estado inicial: {job.status}")

    # 7. Cambiar estado
    job.status = JobStatus.IN_PROGRESS
    print(f"Estado actualizado: {job.status}")

    # 8. Probar Generador de Datos Masivos
    print("\n--- Generando 50 trabajos aleatorios ---")
    mock_jobs = get_mock_workshop_data(num_clients=10, num_jobs=50)
    print(f"Generados {len(mock_jobs)} trabajos.")
    
    sample = mock_jobs[0]
    print(f"Ejemplo: {sample.job_id} | Vehículo: {sample.vehicle.plate} | Cliente: {sample.vehicle.owner.first_name} | Costo: {sample.total_cost:.2f}€")

    print("\n--- Validación Exitosa ---")

if __name__ == "__main__":
    try:
        from universalviewer.domain.workshop import get_mock_workshop_data
        verify()
    except Exception as e:
        import traceback
        traceback.print_exc()
        exit(1)
