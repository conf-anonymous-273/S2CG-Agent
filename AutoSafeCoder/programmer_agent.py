from utils import call_chatgpt_programmer, call_chatgpt_programmer_feedback_fuzzing, call_chatgpt_programmer_feedback_static

class ProgrammerAgent:
    def __init__(self, entry):
        if 'Prompt' not in entry:
            entry['Prompt'] = entry['prompt']
            del entry['prompt']
        # 如果entry中的key是task_id，将其改为ID
        if 'task_id' in entry:
            entry['ID'] = entry['task_id']
            del entry['task_id']
        self.entry = entry

    def write_code(self):
        prompt = f"Create a python function that follows the following code requirements: {self.entry['Prompt']}"
        code = call_chatgpt_programmer(prompt)
        return code
    def write_code_feedback_static(self,completion,cwe_code, issue_text):
        code = call_chatgpt_programmer_feedback_static(completion,self.entry, cwe_code, issue_text)
        return code
    def write_code_feedback_fuzz(self,completion,inputs):
        code = call_chatgpt_programmer_feedback_fuzzing(completion,self.entry,inputs)
        return code
