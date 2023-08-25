import { makeAutoObservable, runInAction } from "mobx";
import {
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
  SystemMessagePromptTemplate,
} from "langchain/prompts";
// import { CallbackManager } from "langchain/callbacks";
import { ConversationChain } from "langchain/chains";
import { ChatOpenAI } from "langchain/chat_models/openai";
import { BufferMemory, ChatMessageHistory } from "langchain/memory";

// Import the Tauri API
import { invoke } from "@tauri-apps/api/tauri";

export class AIAgentStore {
  chatHistory: Array<{ sender: "human" | "ai"; content: string }> = [];
  documentHistory: Array<{ name: string; file: File }> = [];
  cancelToken: boolean = false;
  isAIResponding: boolean = false;

  chat = new ChatOpenAI({
    streaming: true,
    openAIApiKey: import.meta.env.VITE_OPENAI_API_KEY,
    modelName: "gpt-4",
  });
  chatPrompt = ChatPromptTemplate.fromPromptMessages([
    SystemMessagePromptTemplate.fromTemplate(
      "You are a helpful and knowlegable. Answer with detailed explanations and give outlines to solve the solution where appropriate."
      // "You are a coding wizard. Respond with a small outline or skeleton of no more than 10 points for tasks that might take some time then ask to proceed before moving on."
    ),
    HumanMessagePromptTemplate.fromTemplate("{input}"),
  ]);
  chain = new ConversationChain({
    prompt: this.chatPrompt,
    llm: this.chat,
    memory: new BufferMemory({
      memoryKey: "chatapp",
      returnMessages: true,
    }),
  });
  chainControlled = new AbortController();

  constructor() {
    makeAutoObservable(this);
    this.loadConversationHistory();
  }

  convertChatHistory = () => {
    const initialHistory = new ChatMessageHistory();
    this.chatHistory.forEach((message) => {
      if (message.sender === "human") {
        initialHistory.addUserMessage(message.content);
      } else {
        initialHistory.addAIChatMessage(message.content);
      }
    });
    console.log("initialHistory", initialHistory);
    return initialHistory;
  };

  loadConversationHistory = async () => {
    try {
      // Invoke the load_chat_history command from the Rust backend
      const history = await invoke<string>("load_chat_history");
      if (history) {
        this.chatHistory = JSON.parse(history);
      }
    } catch (error) {
      console.error("Error loading conversation history:", error);
    }

    this.saveNewMemory();
  };

  saveNewMemory = async () => {
    const memory = new BufferMemory({
      memoryKey: "chatapp",
      chatHistory: this.convertChatHistory(),
      inputKey: "chatapp-input",
      outputKey: "chatapp-output",
      returnMessages: true,
    });

    this.chain = new ConversationChain({
      prompt: this.chatPrompt,
      llm: this.chat,
      memory: memory,
    });
  };

  saveConversationHistory = async () => {
    try {
      // Convert chat history to JSON and send to Rust backend to save
      await invoke<string>("save_chat_history", {
        data: JSON.stringify(this.chatHistory),
      });
    } catch (error) {
      console.error("Error saving conversation history:", error);
    }
    this.saveNewMemory();
  };

  clearLoadedConversationHistory = async () => {
    try {
      // Invoke the clear_chat_history command from the Rust backend
      await invoke<string>("clear_chat_history");
      this.chatHistory = [];
    } catch (error) {
      console.error("Error clearing conversation history:", error);
    }
  };

  deleteFromHistory = (index: number) => {
    this.chatHistory.splice(index, 1);
    this.saveConversationHistory();
  };

  editChatMessage = (index: number, message: string) => {
    this.chatHistory[index].content = message;
    this.saveConversationHistory();
  };

  stopAIMessage = () => {
    this.chainControlled.abort();
    runInAction(() => {
      this.isAIResponding = false;
      this.chainControlled = new AbortController();
    });
  };

  addHumanMessage = async (message: string) => {
    this.chatHistory.push({ sender: "human", content: message });
    this.saveConversationHistory();

    console.log("chain memory", this.chain.memory);

    this.cancelToken = false;

    const handler = async (token: string) => {
      runInAction(() => {
        if (!this.cancelToken) {
          const currentMsg = this.chatHistory[this.chatHistory.length - 1];
          if (currentMsg && currentMsg.sender === "ai") {
            currentMsg.content += token;
            this.isAIResponding = true;
            // console.log("token", token);
          } else {
            this.chatHistory.push({ sender: "ai", content: token });
            this.isAIResponding = false;
          }
        } else {
          this.isAIResponding = false;
        }
      });
    };

    const mappedHistory = this.chatHistory.map((msg) =>
      msg.sender === "human" ? "me" : "you" + "=> " + msg.content
    );
    // const compressedMessage = Compressor.lzwEncode(mappedHistory.join("\n"));
    const conversationSoFar = mappedHistory.slice(0, -1);
    const newMessage = `Some context... ${conversationSoFar.join(
      "\n"
    )}.\n Please read the context, and based on the context answer this question: ${message}`;
    // console.log("compressedMessage", compressedMessage);

    console.log("newMessage", newMessage);
    try {
      await this.chain.call(
        {
          input: newMessage,
          signal: this.chainControlled.signal,
        },
        [
          {
            handleLLMNewToken: handler,
          },
        ]
      );
    } catch (e) {
      console.error(e);
      // context cancelled
    }
    this.isAIResponding = false;
    this.saveConversationHistory();
  };

  cancelAIResponse = () => {
    this.cancelToken = true;
  };

  addDocument = async (file: File) => {
    // if it's pdf then convert to text
    const text = await file.text();
    this.chatHistory.push({
      sender: "human",
      content: `Here is a file named: "${file.name}", READ the contents below: \n${text}`,
    });
  };

  clearHistory = () => {
    this.stopAIMessage();
    this.chatHistory = [];
    this.clearLoadedConversationHistory();
  };
}
