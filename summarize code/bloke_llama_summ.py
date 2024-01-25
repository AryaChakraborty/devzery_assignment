from langchain.prompts import PromptTemplate

from ctransformers import AutoModelForCausalLM

def getLLamaresponse(code_text):

    ### LLama2 model
    llm = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7B-Chat-GGML", model_file="llama-2-7b-chat.ggmlv3.q8_0.bin")
    
    ## Prompt Template

    template="""
        Write a summary for every function in this code - 
        {code_text}
        """
    
    prompt=PromptTemplate(input_variables=['code_text'],
                          template=template)
    
    ## Generate the ressponse from the LLama 2 model
    response=llm(prompt.format(code_text=code_text))
    # print(response)
    return response

print(getLLamaresponse("def func1(): print('Function 1'); return 1; def func2(): print('Function 2'); return 2; def func3(): print('Function 3'); return 3; func1(); func2(); func3(); def func1(): print('Function 1'); return 1; def func2(): print('Function 2'); return 2; def func3(): print('Function 3'); return 3; func1(); func2(); func3()"))