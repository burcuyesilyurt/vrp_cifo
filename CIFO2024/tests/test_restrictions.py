from unittest import TestCase

from ..restrictions import has_capacity_violation, has_pickup_violation

class PickupViolationTest(TestCase):
    def test_delivery_after_pickup_no_violation(self):
        data = [
            #0
            ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
            #1
            ['C24', 'cd', '25.0', '50.0', '-20.0', '0.0', '1131.0', '90.0', 'C65'],
            #2
            ['C57', 'cd', '40.0', '15.0', '-60.0', '989.0', '1063.0', '90.0', 'C98'],
            #3
            ['C65', 'cp', '48.0', '40.0', '20.0', '67.0', '139.0', '90.0', 'C24'],
            #4
            ['C98', 'cp', '58.0', '75.0', '60.0', '0.0', '1115.0', '90.0', 'C57'],
        ]

        assert (not has_pickup_violation([0, 3, 4, 1, 2], data))

    def test_delivery_after_pickup_violation(self):
        data = [
            #0
            ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
            #1
            ['C24', 'cd', '25.0', '50.0', '-20.0', '0.0', '1131.0', '90.0', 'C65'],
            #2
            ['C57', 'cd', '40.0', '15.0', '-60.0', '989.0', '1063.0', '90.0', 'C98'],
            #3
            ['C65', 'cp', '48.0', '40.0', '20.0', '67.0', '139.0', '90.0', 'C24'],
            #4
            ['C98', 'cp', '58.0', '75.0', '60.0', '0.0', '1115.0', '90.0', 'C57'],
        ]

        assert (has_pickup_violation([0, 3, 1, 2, 4], data))

class CapacityViolationTest(TestCase):
    def test_capacity_not_exceeded(self):
        capacity = 100
        pickup1_capacity = 90
        pickup2_capacity = 10

        data = [
            #0
            ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
            #1
            ['C24', 'cd', '25.0', '50.0', -pickup1_capacity, '0.0', '1131.0', '90.0', 'C65'],
            #2
            ['C57', 'cd', '40.0', '15.0', -pickup2_capacity, '989.0', '1063.0', '90.0', 'C98'],
            #3
            ['C65', 'cp', '48.0', '40.0', pickup1_capacity, '67.0', '139.0', '90.0', 'C24'],
            #4
            ['C98', 'cp', '58.0', '75.0', pickup2_capacity, '0.0', '1115.0', '90.0', 'C57'],
        ]

        assert (not has_capacity_violation([0, 3, 4, 1, 2], data, capacity))


    def test_capacity_exceeded(self):
        capacity = 90
        pickup1_capacity = 90
        pickup2_capacity = 10

        data = [
            #0
            ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
            #1
            ['C24', 'cd', '25.0', '50.0', -pickup1_capacity, '0.0', '1131.0', '90.0', 'C65'],
            #2
            ['C57', 'cd', '40.0', '15.0', -pickup2_capacity, '989.0', '1063.0', '90.0', 'C98'],
            #3
            ['C65', 'cp', '48.0', '40.0', pickup1_capacity, '67.0', '139.0', '90.0', 'C24'],
            #4
            ['C98', 'cp', '58.0', '75.0', pickup2_capacity, '0.0', '1115.0', '90.0', 'C57'],
        ]

        assert (has_capacity_violation([0, 3, 4, 1, 2], data, capacity))

    def test_capacity_not_exceeded_pickup_after_delivery(self):
        capacity = 90
        pickup1_capacity = 90
        pickup2_capacity = 10

        data = [
            #0
            ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
            #1
            ['C24', 'cd', '25.0', '50.0', -pickup1_capacity, '0.0', '1131.0', '90.0', 'C65'],
            #2
            ['C57', 'cd', '40.0', '15.0', -pickup2_capacity, '989.0', '1063.0', '90.0', 'C98'],
            #3
            ['C65', 'cp', '48.0', '40.0', pickup1_capacity, '67.0', '139.0', '90.0', 'C24'],
            #4
            ['C98', 'cp', '58.0', '75.0', pickup2_capacity, '0.0', '1115.0', '90.0', 'C57'],
        ]

        assert (not has_capacity_violation([0, 3, 1, 4, 2], data, capacity))
