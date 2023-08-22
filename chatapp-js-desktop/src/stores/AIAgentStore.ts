import { makeAutoObservable } from "mobx";
import { ChatOpenAI } from "langchain/chat_models/openai";
import { HumanMessage } from "langchain/schema";

export class AIAgentStore {
  chatHistory: Array<{ sender: "human" | "ai"; content: string }> = [];
  documentHistory: Array<{ name: string; file: File }> = [];
  cancelToken: boolean = false;
  isAIResponding: boolean = false;

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

    this.cancelToken = false;

    await this.chat.call([new HumanMessage(message)], {
      callbacks: [
        {
          handleLLMNewToken: (token: string) => {
            if (!this.cancelToken) {
              const currentMsg = this.chatHistory[this.chatHistory.length - 1];
              if (currentMsg && currentMsg.sender === "ai") {
                currentMsg.content += token;
                this.isAIResponding = true;
              } else {
                this.chatHistory.push({ sender: "ai", content: token });
                this.isAIResponding = false;
              }
            } else {
              this.isAIResponding = false;
            }
          },
        },
      ],
    });
    this.isAIResponding = false;

    // this.chatHistory.push({ sender: "ai", content: aiResponse.text.trim() });
  };

  cancelAIResponse = () => {
    this.cancelToken = true;
  };

  addDocument = (file: File) => {
    this.documentHistory.push({ name: file.name, file: file });
  };

  removeDocument = (name: string) => {
    this.documentHistory = this.documentHistory.filter(
      (doc) => doc.name !== name
    );
  };
}
