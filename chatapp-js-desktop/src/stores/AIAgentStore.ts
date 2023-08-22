import { makeAutoObservable } from "mobx";
import {
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
  SystemMessagePromptTemplate,
} from "langchain/prompts";
import { LLMChain } from "langchain/chains";
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
  chatPrompt = ChatPromptTemplate.fromPromptMessages([
    SystemMessagePromptTemplate.fromTemplate(
      "You are a coding wizard. Respond with a small outline or skeleton of no more than 10 points for tasks that might take some time then ask to proceed before moving on."
    ),
    HumanMessagePromptTemplate.fromTemplate("{text}"),
  ]);
  chain = new LLMChain({
    prompt: this.chatPrompt,
    llm: this.chat,
  });
  chainControlled = new AbortController();

  constructor() {
    makeAutoObservable(this);
  }

  stopAIMessage = () => {
    this.chainControlled.abort();
    this.isAIResponding = false;
  };

  addHumanMessage = async (message: string) => {
    this.chatHistory.push({ sender: "human", content: message });

    this.cancelToken = false;

    try {
      // await this.chain.call([new HumanMessage(message)], {
      await this.chain.call(
        {
          text: message,
          signal: this.chainControlled.signal,
        },
        [
          {
            handleLLMNewToken: (token: string) => {
              if (!this.cancelToken) {
                const currentMsg =
                  this.chatHistory[this.chatHistory.length - 1];
                if (currentMsg && currentMsg.sender === "ai") {
                  currentMsg.content += token;
                  this.isAIResponding = true;
                  console.log("token", token);
                } else {
                  this.chatHistory.push({ sender: "ai", content: token });
                  this.isAIResponding = false;
                }
              } else {
                this.isAIResponding = false;
              }
            },
          },
        ]
      );
    } catch (e) {
      console.error(e);
      // context cancelled
    }
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

  clearHistory = () => {
    this.chatHistory = [];
    this.documentHistory = [];
  };
}
