import React from "react";
// import { invoke } from "@tauri-apps/api/tauri";
import { observer, Provider } from "mobx-react";
import "./App.css";
import { rootStore } from "./stores/RootStore";
import { ChatWindow } from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import DocumentHistory from "./components/DocumentHistory";

const App: React.FC = observer(() => {
  return (
    <Provider {...rootStore}>
      <div className="container mx-auto p-8">
        <h1 className="text-3xl font-bold mb-4">Chat Window</h1>

        <ChatWindow />

        <ChatInput />
        <DocumentHistory />
      </div>
    </Provider>
  );
});

export default App;
