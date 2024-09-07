import BooleanSetting from "./BooleanSetting";
import KillSwitch from "./KillSwitch";
import PageArea from "./PageArea";
import { WebsocketSender } from "./util/WebsocketUtil";

interface Props {
  sendMessage: WebsocketSender;
}

const Settings = ({ sendMessage }: Props) => {
  const changeSetting = (id: string, newState: boolean) => {
    sendMessage(JSON.stringify({
      action: "change_setting",
      setting_id: id,
      new_state: newState
    }))
  }

  return (
    <PageArea title="Settings" className="rounded-start">
      <BooleanSetting
        text="Wait for confirmation before each action"
        enabled={false}
        toggleCallback={(newState) => changeSetting("confirmation", newState)}
      />
      <KillSwitch sendMessage={sendMessage}/>
    </PageArea>
  );
};

export default Settings;
