import { Button } from "react-bootstrap";
import { WebsocketSender } from "./util/WebsocketUtil";

interface Props {
  sendMessage: WebsocketSender;
}

const KillSwitch = ({ sendMessage }: Props) => {
  return <Button className="btn-danger" onClick={() => {
    sendMessage(JSON.stringify({
        action: "kill"
    }))
  }}>Kill switch</Button>;
};

export default KillSwitch;
