import unittest
from unittest import mock, TestCase
from unittest.mock import patch, MagicMock

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from src.main import Main


class TestMain(TestCase):

  @patch("builtins.print")
  def test_init(self, mock_print):
    
    os.environ["HOST"] = "http://test"
    os.environ["TOKEN"] = "3RerhuiB8W"
    os.environ["TICKETS"] = "10"
    os.environ["T_MAX"] = "110.10"
    os.environ["T_MIN"] = "85"

    main = Main()

    self.assertEqual(main.HOST, "http://test")
    self.assertEqual(main.TOKEN, "3RerhuiB8W")
    self.assertEqual(main.TICKETS, "10")
    self.assertEqual(main.T_MAX, "110.10")
    self.assertEqual(main.T_MIN, "85")

    # Check if the print is correctly called with the expected output
    mock_print.assert_called_once_with("Token: 3RerhuiB8W; Host: http://test")
  
  @patch("src.main.Main.set_sensor_hub")
  def test_setup(self, mock_set_sensor_hub):
      main = Main()
      main.setup()
      mock_set_sensor_hub.assert_called_once()
  
  @patch("src.main.HubConnectionBuilder")
  @patch("builtins.print")
  def test_set_sensor_hub(self, mock_print, mock_hub_connection_builder):
    # Create a MagicMock object for the HubConnectionBuilder instance
    mock_hub_connection = MagicMock()
    mock_hub_connection_builder.return_value = mock_hub_connection
    
    main = Main()
    main.set_sensor_hub()
    
    # Assert that HubConnectionBuilder was called with the correct URL
    mock_hub_connection_builder.assert_called_once()
    mock_hub_connection.with_url.assert_called_once_with(f"{main.HOST}/SensorHub?token={main.TOKEN}")
    
  @patch("src.main.Main.analyze_datapoint")
  @patch("builtins.print")
  def test_(self, mock_print, mock_analyze_datapoint):
    main = Main()

    # Test case: valid sensor data
    data = [ {"date": "2023-07-05T00:19:17.1400381+00:00", "data": "94.28"}]
    main.on_sensor_data_received("2023-07-05T00:19:17.1400381+00:00", "94.28")
    mock_analyze_datapoint.assert_called_with("2023-07-05T00:19:17.1400381+00:00", 94.28)

    # Test case: empty sensor data
    no_data = []
    main.on_sensor_data_received(no_data)
    # call_args_list --> call --> args[0]
    index_error_found = any(isinstance(call.args[0], IndexError) for call in mock_print.call_args_list)
    self.assertTrue(index_error_found, "IndexError not found")
    
    # Test case: Invalid sensor data
    invalid_data = [{"date": "2023-07-03", "data": "invalid"}]
    main.on_sensor_data_received(invalid_data)
    value_error_found = any(isinstance(call.args[0], ValueError) for call in mock_print.call_args_list)
    self.assertTrue(value_error_found, "ValueError not found")

  @patch("src.main.Main.send_action_to_hvac")
  def test_analyze_datapoint(self, mock_send_action_to_hvac):
    main = Main()
    main.T_MAX = 25.0
    main.T_MIN = 15.0

    # Test case: data < T_MAX AND data > T_MIN
    main.analyze_datapoint("2023-07-03", 20.0)
    mock_send_action_to_hvac.assert_not_called()

    # Test case: data >= T_MAX
    main.analyze_datapoint("2023-07-01", 30.0)
    mock_send_action_to_hvac.assert_called_once_with("2023-07-01", "TurnOnAc", main.TICKETS)

    # Test case: data <= T_MIN
    main.analyze_datapoint("2023-07-02", 10.0)
    mock_send_action_to_hvac.assert_called_with("2023-07-02", "TurnOnHeater", main.TICKETS)

  @patch("src.main.requests.get")
  @patch("builtins.print")
  def test_send_action_to_hvac(self, mock_print, mock_get):
    main = Main()

    # Create a mock response with a valid JSON string
    mock_response = MagicMock()
    mock_response.text = '{"Response": "Activating Heater for 20 ticks"}'

    mock_get.return_value = mock_response

    main.send_action_to_hvac("2023-07-01", "TurnOnAc", main.TICKETS)

    mock_get.assert_called_once_with(f"{main.HOST}/api/hvac/{main.TOKEN}/TurnOnAc/{main.TICKETS}")

    # Check if the print is correctly called with the expected output
    second_call_args = mock_print.call_args_list[1]  
    self.assertEqual(second_call_args, mock.call({'Response': 'Activating Heater for 20 ticks'}))

if __name__ == "__main__":
    unittest.main()
