import { makeAutoObservable } from "mobx";
import { ChatStore } from "./ChatStore";
import { UserInputStore } from "./UserInputStore";
import { AIAgentStore } from "./AIAgentStore";

class RootStore {
  chatStore = new ChatStore();
  userInputStore = new UserInputStore();
  aiAgentStore = new AIAgentStore();

  constructor() {
    makeAutoObservable(this);
  }
}

export const rootStore = new RootStore();
