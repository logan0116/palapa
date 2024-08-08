from openai import OpenAI
import time


def text_generation(each_prompt: list, mode='gpt'):
    """
    example

    curl https://api.openai.com/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d '{
        "model": "No models available",
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful assistant."
          },
          {
            "role": "user",
            "content": "Hello!"
          }
        ]
      }'

    :param each_prompt:
    :param mode:
    :return:
    """
    if mode == 'gpt':
        model_engine = "gpt-3.5-turbo"
        client = OpenAI(api_key="")
    elif mode == 'deepseek':
        model_engine = "deepseek-chat"
        client = OpenAI(api_key="",
                        base_url="https://api.deepseek.com/")
    else:
        raise ValueError('mode should be gpt or deepseek')

    start_time = time.time()
    response = client.chat.completions.create(
        model=model_engine,
        messages=each_prompt
    )
    end_time = time.time()
    message = response.choices[0].message.content
    print('time: ', end_time - start_time)
    print(message)
    if end_time - start_time < 10:
        time.sleep(10 - (end_time - start_time))
    return message
