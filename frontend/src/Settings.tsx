import BooleanSetting from "./BooleanSetting";
import PageArea from "./PageArea";

interface Props {
  sendMessage: (message: string) => void;
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
    </PageArea>
  );
};

export default Settings;
