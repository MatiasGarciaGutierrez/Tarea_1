from DescriptorAdministrator import CommercialDescriptors
from DescriptorAdministrator import TelevisionDescriptors


def create_all_commercial_descriptors(descriptors_path='descriptors/commercials/', commercial_path='commercials/'):
    commercial_manager = CommercialDescriptors(descriptors_path, commercial_path)
    commercial_manager.create_all_descriptors()


def create_all_television_descriptors(_descriptor_path='descriptors/television/', _videos_path='television/'):
    television_manager = TelevisionDescriptors(_descriptor_path, _videos_path)
    television_manager.create_all_descriptors()


if __name__ == "__main__":
    create_all_commercial_descriptors()
    create_all_television_descriptors()