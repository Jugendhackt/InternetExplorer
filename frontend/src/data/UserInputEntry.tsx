import { ReactNode } from "react";
import { HistoryEntry } from "./HistoryEntry";
import { Card, CardBody, CardSubtitle, CardText } from "react-bootstrap";
import { Chat, Mic } from "react-bootstrap-icons";

export class UserInputEntry extends HistoryEntry {
    inputType: UserInputType;
    inputText: string;
  
    constructor(inputType: UserInputType, inputText: string) {
      super();
      this.inputType = inputType;
      this.inputText = inputText;
    }
  
    render(): ReactNode {
      return (
        <Card className="m-1 w-75 ms-auto clickable-card">
          <CardBody>
            <CardSubtitle className="text-body-secondary mb-2">
              {getInputTypeIcon(this.inputType)}
              {formatUserInputType(this.inputType)}
            </CardSubtitle>
            <CardText>{this.inputText}</CardText>
          </CardBody>
        </Card>
      );
    }
  }
  
  export type UserInputType = "voice" | "text";
  
  function formatUserInputType(type: UserInputType) {
    return type.charAt(0).toUpperCase() + type.slice(1);
  }
  
  function getInputTypeIcon(type: UserInputType): ReactNode {
    switch (type) {
      case "voice":
        return <Mic />;
      case "text":
        return <Chat />;
    }
  }