from transformers import pipeline
import pandas as pd

class CommandSummary():
    """
    For commands extraction we are using LaMini model based on google's 
    T5 Model.
    """
    def __init__(self,model_path):
        """
        model path if it is in local repor or else 
        model_path = 'MBZUAI/LaMini-T5-738M'
        """
        self.checkpoint = model_path
        self.model = pipeline('text2text-generation', model = self.checkpoint)

    def commands_summary_gen(self,commands_list):
        """
        Generating summary of the commands extracted
        """
        command_summaries = []
        for command in commands_list:
            input_prompt = f"""explain the following command in shortest possible and don't give wrong answer:  {command}"""
            generated_text = self.model(input_prompt, max_length=512, do_sample=True)[0]['generated_text']
            command_summaries.append(generated_text)
            print('summary generated for',command)
        data_frame = pd.DataFrame([commands_list,command_summaries],index=['command\query','summary']).T

        # for front end
        front_end_data = [commands_list,command_summaries]
        # print("Response:", generated_text)
        print(front_end_data)
        print(data_frame)
        return data_frame,front_end_data
            

    def regenerate_summary(self,command,df):
        """
        To generate replacement text if user enters command
        """
        input_prompt = f"""explain the following command in shortest possible and don't give wrong answer:  {command}"""
        replacement_text = self.model(input_prompt, max_length=512, do_sample=True)[0]['generated_text']
        print(replacement_text)
        df.loc[df['command\query']==command,'summary'] = replacement_text
        return df,replacement_text
        
        
summ = CommandSummary(model_path=r"../../code_explanataion_model/LaMini-T5-738M/",)
#commands = ['git add .', 'git commit -m "Prime Number Code"', 'git push origin main', 'git push', 'git status', 'git help,']
df,front_end_dat = summ.commands_summary_gen(commands)


new_df,replacement_text = summ.regenerate_summary('git push',df)        