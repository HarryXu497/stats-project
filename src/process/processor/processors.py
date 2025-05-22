from abc import ABC, abstractmethod

class Processor(ABC):
    @abstractmethod
    def process(self, content: str):
        pass


class SpaceSeparatedTextNoLabelProcessor(Processor):
    col_names = [
        "area",
        "composite_hpi",
        "single_family_detached_hpi",
        "single_family_attached_hpi",
        "townhouse_hpi",
        "apartment_hpi",
    ]

    labels = [
        "Toronto W01",
        "Toronto W02",
        "Toronto W03",
        "Toronto W04",
        "Toronto W05",
        "Toronto W06",
        "Toronto W07",
        "Toronto W08",
        "Toronto W09",
        "Toronto W10",
        "Toronto C01",
        "Toronto C02",
        "Toronto C03",
        "Toronto C04",
        "Toronto C06",
        "Toronto C07",
        "Toronto C08",
        "Toronto C09",
        "Toronto C10",
        "Toronto C11",
        "Toronto C12",
        "Toronto C13",
        "Toronto C14",
        "Toronto C15",
        "Toronto E01",
        "Toronto E02",
        "Toronto E03",
        "Toronto E04",
        "Toronto E05",
        "Toronto E06",
        "Toronto E07",
        "Toronto E08",
        "Toronto E09",
        "Toronto E10",
        "Toronto E11",
    ]

    def process(self, content):
        lines = content.splitlines()
        output_lines = []

        if len(lines) != len(self.labels):
            raise ValueError(f"Dimension of data ({len(lines)}) does not match dimension of labels ({len(self.labels)}).")
        
        # Header Row
        output_lines.append(",".join(self.col_names))

        for label, line in zip(self.labels, lines):
            row = line.split(" ")

            output_lines.append(f"{label},{row[0]},{row[3]},{row[6]},{row[9]},{row[12]}")
        
        return "\n".join(output_lines)


