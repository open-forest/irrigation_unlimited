"""Test Irrigation Unlimited manual run service calls."""

# pylint: disable=too-many-lines
from unittest.mock import patch
import homeassistant.core as ha
from homeassistant.const import (
    STATE_OFF,
    STATE_ON,
)
from tests.iu_test_support import (
    IUExam,
    mk_local,
)
from custom_components.irrigation_unlimited.const import (
    SERVICE_MANUAL_RUN,
    SERVICE_TIME_ADJUST,
)
from custom_components.irrigation_unlimited.irrigation_unlimited import (
    IULogger,
)

IUExam.quiet_mode()


# pylint: disable=unused-argument
# pylint: disable=too-many-statements
async def test_service_manual_run_basic(
    hass: ha.HomeAssistant, skip_dependencies, skip_history
):
    """Test manual_run service call."""

    async with IUExam(hass, "service_manual_run.yaml") as exam:
        await exam.begin_test(1)
        await exam.run_until("2021-01-04 06:00:29")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "time": "00:10"},
        )
        await exam.run_until("2021-01-04 06:05:00")
        run = exam.coordinator.controllers[0].runs.current_run
        assert run.schedule_name == "Manual"
        assert run.sequence_adjustment() is None
        await exam.finish_test()

        await exam.begin_test(2)
        await exam.run_until("2021-01-04 08:00:29")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_m", "time": "00:10"},
        )
        await exam.finish_test()

        await exam.begin_test(3)
        await exam.run_until("2021-01-04 06:00:29")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c2_m",
                "time": "00:21",
                "sequence_id": 1,
            },
        )
        await exam.finish_test()

        await exam.begin_test(4)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c2_m",
                "time": "00:01",
                "sequence_id": 1,
            },
        )
        await exam.finish_test()

        with patch.object(IULogger, "_format") as mock:
            await exam.begin_test(5)
            await exam.call(
                SERVICE_MANUAL_RUN,
                {
                    "entity_id": "binary_sensor.irrigation_unlimited_c2_m",
                    "time": "00:01",
                    "sequence_id": 2,
                },
            )
            await exam.finish_test()
            assert (
                sum(
                    [1 for call in mock.call_args_list if call.args[1] == "SEQUENCE_ID"]
                )
                == 1
            )

        await exam.begin_test(6)
        await exam.run_until("2021-01-04 06:15:00")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z2", "time": "00:10"},
        )
        await exam.finish_test()

        await exam.begin_test(7)
        await exam.run_until("2021-01-04 06:15:00")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z2", "time": "00:10"},
        )
        await exam.run_until("2021-01-04 06:20:00")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z2", "time": "00:10"},
        )
        await exam.finish_test()

        await exam.begin_test(8)
        await exam.run_until("2021-01-04 06:15:00")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z2", "time": "00:10"},
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z2", "time": "00:10"},
        )
        await exam.finish_test()

        await exam.begin_test(9)
        await exam.run_until("2021-01-04 08:14:59")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1"},
        )
        await exam.finish_test()

        await exam.begin_test(10)
        await exam.run_until("2021-01-04 08:14:59")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "time": "00:00"},
        )
        await exam.finish_test()

        await exam.begin_test(11)
        await exam.run_until("2021-01-04 08:14:59")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z2"},
        )
        await exam.finish_test()

        await exam.begin_test(12)
        await exam.run_until("2021-01-04 08:14:59")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z2", "time": "00:00"},
        )
        await exam.finish_test()

        await exam.begin_test(13)
        await exam.run_until("2021-01-04 08:14:59")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c2_z1"},
        )
        await exam.finish_test()

        await exam.begin_test(14)
        await exam.call(
            SERVICE_TIME_ADJUST,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "percentage": 50},
        )
        await exam.run_until("2021-01-04 08:14:59")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1"},
        )
        await exam.run_until("2021-01-04 08:30:00")
        await exam.call(
            SERVICE_TIME_ADJUST,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "reset": None},
        )
        await exam.finish_test()

        await exam.begin_test(15)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "time": "00:10"},
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "time": "00:15"},
        )
        await exam.finish_test()

        # Sequence_id is a string and not an integer
        await exam.begin_test(16)
        await exam.run_until("2021-01-04 06:00:29")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c2_m",
                "time": "00:21",
                "sequence_id": '1',
            },
        )
        await exam.finish_test()

        exam.check_summary()


async def test_service_manual_run_negative_preamble(
    hass: ha.HomeAssistant, skip_dependencies, skip_history
):
    """Test manual_run service call on a sequence with negative preamble"""

    async with IUExam(hass, "service_manual_run_negative_preamble.yaml") as exam:
        await exam.begin_test(1)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "time": "00:10"},
        )
        await exam.finish_test()

        await exam.begin_test(2)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1"},
        )
        await exam.finish_test()

        await exam.begin_test(3)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_z1",
                "time": "0:00:00",
            },
        )
        await exam.finish_test()

        await exam.begin_test(4)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "sequence_id": 1,
                "time": "0:22:00",
            },
        )
        await exam.finish_test()

        await exam.begin_test(5)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "sequence_id": 1,
            },
        )
        await exam.finish_test()

        await exam.begin_test(6)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "sequence_id": 1,
                "time": "0:00:00",
            },
        )
        await exam.finish_test()

        await exam.begin_test(7)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "sequence_id": 2,
            },
        )
        await exam.finish_test()

        await exam.begin_test(8)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "sequence_id": 3,
            },
        )
        await exam.finish_test()

        exam.check_summary()


async def test_service_manual_run_queue(
    hass: ha.HomeAssistant, skip_dependencies, skip_history
):
    """Test manual_run service call with queued requests"""

    async with IUExam(hass, "service_manual_run_queue.yaml") as exam:
        await exam.begin_test(1)
        exam.check_iu_entity(
            "c1_z1",
            STATE_OFF,
            {
                "status": "off",
                "current_schedule": None,
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-04 09:05:00"),
                "next_duration": "0:10:00",
            },
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "time": "00:10"},
        )
        await exam.run_until("2023-10-04 06:00:01")
        exam.check_iu_entity(
            "c1_z1",
            STATE_ON,
            {
                "status": "on",
                "current_schedule": 0,
                "current_name": "Manual",
                "current_start": mk_local("2023-10-04 06:00:01"),
                "current_duration": "0:10:00",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-04 09:05:00"),
                "next_duration": "0:10:00",
            },
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_z1",
                "time": "00:15",
                "delay": 10,
            },
        )
        exam.check_iu_entity(
            "c1_z1",
            STATE_ON,
            {
                "status": "on",
                "schedule_count": 1,
                "current_schedule": 0,
                "current_name": "Manual",
                "current_start": mk_local("2023-10-04 06:00:01"),
                "current_duration": "0:10:00",
                "next_schedule": 0,
                "next_name": "Manual",
                "next_start": mk_local("2023-10-04 06:10:11"),
                "next_duration": "0:15:00",
            },
        )
        await exam.run_until("2023-10-04 06:30")
        exam.check_iu_entity(
            "c1_z1",
            STATE_OFF,
            {
                "status": "off",
                "current_schedule": None,
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-04 09:05:00"),
                "next_duration": "0:10:00",
            },
        )
        await exam.finish_test()

        await exam.begin_test(2)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "sequence_id": 1,
            },
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "sequence_id": 1,
                "delay": 5,
            },
        )
        await exam.finish_test()

        await exam.begin_test(3)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {"entity_id": "binary_sensor.irrigation_unlimited_c1_z1", "time": "00:10"},
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "sequence_id": 1,
                "delay": 2,
            },
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_z1",
                "time": "00:10",
                "delay": 3,
            },
        )
        await exam.finish_test()

        await exam.begin_test(4)
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_m",
                "time": "00:10",
            },
        )
        await exam.finish_test()

        await exam.begin_test(5)
        await exam.run_until("2023-10-04 12:05")
        exam.check_iu_entity(
            "c1_z1",
            STATE_OFF,
            {
                "status": "off",
                "current_schedule": None,
                "percent_complete": 0,
                "next_adjustment": "",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-05 09:05:00"),
                "next_duration": "0:10:00",
            },
        )
        exam.check_iu_entity(
            "c1_z2",
            STATE_OFF,
            {
                "status": "off",
                "current_schedule": None,
                "percent_complete": 0,
                "next_adjustment": "",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-05 10:05:00"),
                "next_duration": "0:10:00",
            },
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_z1",
                "time": "00:15",
            },
        )
        await exam.run_until("2023-10-04 12:05:01")
        exam.check_iu_entity(
            "c1_z1",
            STATE_ON,
            {
                "status": "on",
                "current_adjustment": "",
                "current_schedule": 0,
                "current_name": "Manual",
                "current_start": mk_local("2023-10-04 12:05:01"),
                "current_duration": "0:15:00",
                "next_adjustment": "",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-05 09:05:00"),
                "next_duration": "0:10:00",
            },
        )
        exam.check_iu_entity(
            "c1_z2",
            STATE_OFF,
            {
                "status": "off",
                "current_schedule": None,
                "next_adjustment": "",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-05 10:05:00"),
                "next_duration": "0:10:00",
            },
        )
        await exam.run_until("2023-10-04 12:10")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_z2",
                "time": "00:15",
            },
        )
        exam.check_iu_entity(
            "c1_z1",
            STATE_ON,
            {
                "status": "on",
                "current_adjustment": "",
                "current_schedule": 0,
                "current_name": "Manual",
                "current_start": mk_local("2023-10-04 12:05:01"),
                "current_duration": "0:15:00",
                "next_adjustment": "",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-05 09:05:00"),
                "next_duration": "0:10:00",
            },
        )
        exam.check_iu_entity(
            "c1_z2",
            STATE_OFF,
            {
                "status": "off",
                "current_schedule": None,
                "percent_complete": 0,
                "next_adjustment": "",
                "next_schedule": 0,
                "next_name": "Manual",
                "next_start": mk_local("2023-10-04 12:20:01"),
                "next_duration": "0:15:00",
            },
        )
        await exam.run_until("2023-10-04 12:40")
        exam.check_iu_entity(
            "c1_z1",
            STATE_OFF,
            {
                "status": "off",
                "current_schedule": None,
                "next_adjustment": "",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-05 09:05:00"),
                "next_duration": "0:10:00",
            },
        )
        exam.check_iu_entity(
            "c1_z2",
            STATE_OFF,
            {
                "status": "off",
                "current_schedule": None,
                "percent_complete": 0,
                "next_adjustment": "",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-05 10:05:00"),
                "next_duration": "0:10:00",
            },
        )
        await exam.finish_test()

        await exam.begin_test(6)
        await exam.run_until("2023-10-04 12:05")
        exam.check_iu_entity(
            "c1_s1",
            STATE_OFF,
            {
                "current_zone": None,
                "current_schedule": None,
                "next_start": mk_local("2023-10-05 11:05:00"),
                "next_duration": "0:27:00",
                "next_schedule": 1,
                "next_name": "Schedule 1",
            },
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_s1",
                "time": "0:19:00",
            },
        )
        await exam.run_until("2023-10-04 12:05:01")
        exam.check_iu_entity(
            "c1_s1",
            STATE_ON,
            {
                "status": "on",
                "current_zone": 1,
                "current_start": mk_local("2023-10-04 12:05:01"),
                "current_duration": "0:19:00",
                "current_schedule": 0,
                "current_name": "Manual",
                "next_start": mk_local("2023-10-05 11:05:00"),
                "next_duration": "0:27:00",
                "next_schedule": 1,
                "next_name": "Schedule 1",
            },
        )
        await exam.run_until("2023-10-04 12:12")
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_s1",
                "time": "0:19:00",
            },
        )
        await exam.run_until("2023-10-04 12:12:01")
        exam.check_iu_entity(
            "c1_s1",
            STATE_ON,
            {
                "status": "on",
                "current_zone": 2,
                "current_start": mk_local("2023-10-04 12:05:01"),
                "current_duration": "0:19:00",
                "current_schedule": 0,
                "current_name": "Manual",
                "next_start": mk_local("2023-10-04 12:24:01"),
                "next_duration": "0:19:00",
                "next_schedule": 0,
                "next_name": "Manual",
            },
        )
        await exam.finish_test()

        await exam.begin_test(7)
        await exam.run_until("2023-10-04 09:10")
        exam.check_iu_entity(
            "c1_z1",
            STATE_ON,
            {
                "current_schedule": 1,
                "current_name": "Schedule 1",
                "current_start": mk_local("2023-10-04 09:05:00"),
                "current_duration": "0:10:00",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-04 11:05:00"),
                "next_duration": "0:06:00",
            },
        )
        await exam.call(
            SERVICE_MANUAL_RUN,
            {
                "entity_id": "binary_sensor.irrigation_unlimited_c1_z1",
                "time": "00:15",
            },
        )
        exam.check_iu_entity(
            "c1_z1",
            STATE_ON,
            {
                "current_schedule": 0,
                "current_name": "Manual",
                "current_start": mk_local("2023-10-04 09:10:00"),
                "current_duration": "0:15:00",
                "next_schedule": 1,
                "next_name": "Schedule 1",
                "next_start": mk_local("2023-10-04 11:05:00"),
                "next_duration": "0:06:00",
            },
        )
        await exam.finish_test()

        exam.check_summary()
