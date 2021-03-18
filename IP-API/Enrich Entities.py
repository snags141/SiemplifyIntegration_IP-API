from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
from IP_APIManager import IP_APIManager
import json

@output_handler
def main():
    siemplify = SiemplifyAction()

    verify_ssl = siemplify.extract_configuration_param('Integration',"Verify SSL", input_type=bool)
    query_parameters = siemplify.extract_action_param("Query Parameters", print_value=True)
    api_key = ""
    
    ipapi = IP_APIManager(api_key, verify_ssl)
    json_response = ipapi.check_ip(query_parameters)
    
    status = EXECUTION_STATE_COMPLETED
    output_message = "success"
    result_value = "success"
    siemplify.result.add_result_json({'Results': [json_response]})
    siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()

