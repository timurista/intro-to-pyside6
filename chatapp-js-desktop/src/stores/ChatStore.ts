import { makeAutoObservable } from "mobx";

export class ChatStore {
  messages: Array<{
    type: "text" | "document";
    content: string;
    nestedItems?: Array<string>;
  }> = [];

  constructor() {
    makeAutoObservable(this);
  }

  clearHistory = () => {
    this.messages = [];
  };

  addMessage = (message: {
    type: "text" | "document";
    content: string;
    nestedItems?: Array<string>;
  }) => {
    this.messages.push(message);
  };
}
