import { makeAutoObservable } from "mobx";

export class UserInputStore {
  input: string = "";
  documentName: string | null = null;
  nestedItems: Array<string> = [];

  constructor() {
    makeAutoObservable(this);
  }

  setInput = (value: string) => {
    this.input = value;
  };

  setDocumentName = (name: string | null) => {
    this.documentName = name;
  };

  addNestedItem = (item: string) => {
    this.nestedItems.push(item);
  };

  clearInput = () => {
    this.input = "";
    this.documentName = null;
    this.nestedItems = [];
  };
}
