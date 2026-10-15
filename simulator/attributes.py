import random


AGE_GROUPS = ["child", "adult", "older_adult"]

DEPARTMENTS = [
	"Emergency",
	"Radiology",
	"Laboratory",
]

RESOURCES = [
	"Nurse",
	"Doctor",
	"Radiology Technician",
	"Lab Technician",
]


def generate_patient_attributes(rng=None):
	"""Return simulated attributes for one patient.

	Args:
		rng: Optional random number generator for reproducible results.

	Returns:
		A dictionary containing an age group, department, and resource.
	"""
	if rng is None:
		rng = random.Random()

	return {
		"age_group": rng.choice(AGE_GROUPS),
		"department": rng.choice(DEPARTMENTS),
		"resource": rng.choice(RESOURCES),
	}


if __name__ == "__main__":
	rng = random.Random(42)

	for patient_number in range(1, 6):
		attributes = generate_patient_attributes(rng)
		print(f"Patient {patient_number}: {attributes}")
