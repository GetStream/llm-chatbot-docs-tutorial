# Create LLM-powered Chatbot For Your Documentation

This repository contains the code for the blog post originally published on the Stream blog [here](https://www.getstream.io/blog/llm-chatbot-doc).

All the background can be found there.

## 🛠️ Project Setup

To get the project up and running, follow the [post](https://getstream.io/blog/llm-chatbot-doc/). In addition, you need two things:

1. a Python setup with the required packages installed.
2. an OpenAI API key

A more thorough explanation can be found in the blog post but here are the quick commands to set up Python (we tested with version 3.9). Run the following commands in your project folder:

```bash
python -m venv llm-env
source llm-env/bin/activate # this is for macOS/Linux, on Windows run llm-env/bin/activate
pip install -r requirements.txt
```

Then, get your OpenAI API key from [their site](https://openai.com/blog/openai-api). Once you have it, open up `.env.local` and replace `<add-openai-api-key-here>` with your key (no `"` needed).

With that, you have the project ready to run. Enjoy using it and [let us know](https://twitter.com/getstream_io) what you build with it.

## 🛥 What is Stream?

Stream allows developers to rapidly deploy scalable feeds, chat messaging, and video with an industry-leading 99.999% uptime SLA guarantee.

Stream provides UI components and state handling that make it easy to build video calling for your app. All calls run on Stream’s network of edge servers around the world, ensuring optimal latency and reliability.

## 👩‍💻 Free for Makers 👨‍💻

Stream is free for most side and hobby projects. To qualify, your project/company needs to have < 5 team members and < $10k in monthly revenue. Makers get $100 in monthly credit for video for free. For more details, check out the [Maker Account](https://getstream.io/maker-account).
