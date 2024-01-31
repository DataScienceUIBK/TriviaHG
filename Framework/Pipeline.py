import os
from utils.Hint_Generation.Hint_Generation import Hint_Generation
from utils.Hint_Evaluation.Hint_Evaluation import Hint_Evaluation
from utils.Clean_File import Clean_File
from termcolor import colored


def main():
    base_url = "https://api.endpoints.anyscale.com/v1"
    api_key = ""
    models = ['LLaMA_7b_Vanilla', 'LLaMA_7b_Finetuned', 'LLaMA_13b_Vanilla', 'LLaMA_13b_Finetuned', 'LLaMA_70b_Vanilla',
              'LLaMA_70b_Finetuned']

    if not os.path.exists('./outputs'):
        os.mkdir('./outputs')

    for model in models:
        print(colored(f'{model}:', attrs=['bold'], color='green'))
        print()
        hint_generation = Hint_Generation(base_url=base_url, api_key=api_key, model=model)
        hint_generation.generate()

        hint_evaluation = Hint_Evaluation(base_url=base_url, api_key=api_key, model=model)
        hint_evaluation.evaluate()

        clean_file = Clean_File(model)
        clean_file.clean()

        print()
        print()


if __name__ == '__main__':
    main()
