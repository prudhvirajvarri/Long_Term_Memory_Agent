import pytest
from unittest.mock import patch, MagicMock
import json

@patch('main.client.chat.completions.create')
def test_conversation_triggers_create_memory(mock_openai_create):
    mock_tool_call_response = MagicMock()
    tool_call = MagicMock()
    tool_call.id = "call_abc123"
    tool_call.function.name = "create_memory"
    tool_call.function.arguments = json.dumps({"content": "I use Shram as a productivity tool."})
    mock_tool_call_response.choices[0].message.tool_calls = [tool_call]
    
    mock_final_response = MagicMock()
    mock_final_response.choices[0].message.content = "Got it! I've remembered that you use Shram."

    mock_openai_create.side_effect = [mock_tool_call_response, mock_final_response]

    mock_create_memory_func = MagicMock(return_value="Memory created successfully.")

    with patch.dict('main.functions', {'create_memory': mock_create_memory_func}):
        with patch('builtins.input', side_effect=['I use Shram as a productivity tool.', 'exit']):
            from io import StringIO
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            from main import conversation_loop
            conversation_loop()
            
            sys.stdout = old_stdout
            final_output = captured_output.getvalue()

    mock_create_memory_func.assert_called_once_with(content="I use Shram as a productivity tool.")
    assert "Got it! I've remembered that you use Shram." in final_output
    