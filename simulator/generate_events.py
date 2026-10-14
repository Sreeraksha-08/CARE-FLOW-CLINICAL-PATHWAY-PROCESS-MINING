import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yaml


def load_config():
	"""Load simulator settings from config.yaml."""
	config_path = Path(__file__).with_name("config.yaml")

	with config_path.open("r", encoding="utf-8") as file:
		return yaml.safe_load(file)


def generate_patient_journey(case_number, scenario, config, rng):
	"""Generate one simulated patient's chronological activity events."""
	journey = config["journey"]
	scenarios = config["scenarios"]

	case_id = f"ER{case_number:05d}"
	start_time = datetime(2026, 1, 1, 8, 0, 0) + timedelta(
		minutes=rng.randint(0, 60 * 24 * 30)
	)

	activities = journey["activities"]
	loopback_probability = scenarios[scenario]["loopback_probability"]
	has_loopback = rng.random() < loopback_probability
	has_lab_test = rng.random() < journey["lab_test_probability"]

	events = []
	current_time = start_time

	for activity in activities:
		events.append({
			"case_id": case_id,
			"activity": activity,
			"timestamp": current_time,
			"scenario": scenario,
			"loopback_reason": None,
		})

		# Simulate a repeat X-Ray followed by a return to Triage.
		if activity == "X-Ray" and has_loopback:
			current_time += timedelta(minutes=rng.randint(10, 45))
			events.append({
				"case_id": case_id,
				"activity": "Triage",
				"timestamp": current_time,
				"scenario": scenario,
				"loopback_reason": "missing_paperwork_form",
			})

		# Add an optional Lab Test after Doctor Consultation.
		if activity == "Doctor Consultation" and has_lab_test:
			current_time += timedelta(minutes=rng.randint(15, 60))
			events.append({
				"case_id": case_id,
				"activity": "Lab Test",
				"timestamp": current_time,
				"scenario": scenario,
				"loopback_reason": None,
			})

		current_time += timedelta(minutes=rng.randint(5, 90))

	return events


def main():
	parser = argparse.ArgumentParser(
		description="Generate simulated CareFlow patient event logs."
	)
	parser.add_argument(
		"--scenario",
		choices=["before", "after"],
		default="before",
		help="Choose before or after the process improvement.",
	)
	parser.add_argument(
		"--cases",
		type=int,
		default=None,
		help="Number of simulated patient cases.",
	)
	parser.add_argument(
		"--output",
		default=None,
		help="CSV output path.",
	)
	args = parser.parse_args()

	config = load_config()
	number_of_cases = args.cases or config["simulation"]["default_cases"]

	if number_of_cases < 1:
		parser.error("--cases must be at least 1")

	seed = config["simulation"]["random_seed"]
	rng = random.Random(seed)

	all_events = []
	for case_number in range(1, number_of_cases + 1):
		all_events.extend(
			generate_patient_journey(
				case_number, args.scenario, config, rng
			)
		)

	df = pd.DataFrame(all_events)
	df = df.sort_values(["case_id", "timestamp"]).reset_index(drop=True)

	output_path = Path(
		args.output
		or f"sample_data/{args.scenario}_events.csv"
	)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	df.to_csv(output_path, index=False)

	print(f"Scenario: {args.scenario}")
	print(f"Patient cases: {number_of_cases}")
	print(f"Total events: {len(df)}")
	print(f"Saved event log to: {output_path}")
	print("\nFirst 10 events:")
	print(df.head(10).to_string(index=False))


if __name__ == "__main__":
	main()
