import BooleanSetting from "./BooleanSetting";
import PageArea from "./PageArea";

const Settings = () => {
  return (
    <PageArea title="Settings" className="rounded-start">
      <BooleanSetting
        text="Wait for confirmation before each action"
        enabled={false}
      />
    </PageArea>
  );
};

export default Settings;
