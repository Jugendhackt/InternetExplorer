import { ReactNode } from "react";
import { HistoryEntry } from "./HistoryEntry";
import { Card, CardBody, CardSubtitle, CardText } from "react-bootstrap";
import { BrowserChrome, Keyboard, Mouse } from "react-bootstrap-icons";

export class BrowseActionEntry extends HistoryEntry {
  render(): ReactNode {
    throw new Error("Method not implemented.");
  }

  actions: BrowseAction[];

  constructor(actions: BrowseAction[]) {
    super();
    this.actions = actions;
  }
}

interface Props {
  browseActionEntry: BrowseActionEntry;
  setActionDetails: (actionDetails: Map<string, string>) => void;
}

const BrowseActionEntryComponent = ({browseActionEntry, setActionDetails}: Props) => {
  return (
    <Card className="m-1 w-75 me-auto">
        <CardBody>{browseActionEntry.actions.map((action) => action.render(setActionDetails))}</CardBody>
    </Card>
  )
}

export default BrowseActionEntryComponent


// TODO implement all types
export type BrowseActionType = string; //"click_element" | "await_loading";
export type BrowseActionResult = "success" | "failure";

function getBrowseActionTypeIcon(
  browseActionType: BrowseActionType
): ReactNode {
  switch (browseActionType) {
    case "click_element":
      return <Mouse />;
    case "open_website":
      return <BrowserChrome />;
    case "type_text":
      return <Keyboard />
  }
}

function formatBrowseActionType(browseActionType: BrowseActionType): string {
  return browseActionType; // TODO implement
}

export class BrowseAction {
  type: BrowseActionType;
  actionData: Map<string, string>;
  result: BrowseActionResult;

  constructor(
    type: BrowseActionType,
    actionData: Map<string, string>,
    result: BrowseActionResult
  ) {
    this.type = type;
    this.actionData = actionData;
    this.result = result;
  }

  render(setActionDetails: (actionDetails: Map<string, string>) => void): ReactNode {
    return (
      <Card onClick={() => {
        setActionDetails(this.actionData);
      }}>
        <CardBody>
          <CardSubtitle className="text-body-secondary mb-2">
            {getBrowseActionTypeIcon(this.type)}
            {formatBrowseActionType(this.type)}
          </CardSubtitle>
          <CardText>test123</CardText>
        </CardBody>
      </Card>
    );
  }
}
