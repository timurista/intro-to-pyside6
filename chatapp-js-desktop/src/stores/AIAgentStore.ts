import { makeAutoObservable } from "mobx";
import { ChatOpenAI } from "langchain/chat_models/openai";
import { HumanMessage } from "langchain/schema";

console.log({ env: import.meta.env });

export class AIAgentStore {
  chatHistory: Array<{ sender: "human" | "ai"; content: string }> = [];
  chat = new ChatOpenAI({
    maxTokens: 250,
    streaming: true,
    openAIApiKey: import.meta.env.VITE_OPENAI_API_KEY,
  });

  constructor() {
    makeAutoObservable(this);
  }

  addHumanMessage = async (message: string) => {
    this.chatHistory.push({ sender: "human", content: message });

    const aiResponse = await this.chat.call([new HumanMessage(message)], {
      callbacks: [
        {
          handleLLMNewToken(token: string) {
            console.log({ token });
          },
        },
      ],
    });

    this.chatHistory.push({ sender: "ai", content: aiResponse.text.trim() });
  };
}
