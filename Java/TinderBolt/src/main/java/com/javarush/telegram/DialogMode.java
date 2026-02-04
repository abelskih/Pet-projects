package com.javarush.telegram;

public enum DialogMode {

    MAIN("/start"),
    PROFILE("/profile"),
    OPENER("/opener"),
    MESSAGE("/message"),
    DATE("/date"),
    GPT("/gpt"),
    NONE(null);

    private final String command;

    DialogMode(String command) {
        this.command = command;
    }

    public String getCommand() {
        return command;
    }

    public static DialogMode fromCommand(String command) {
        for (DialogMode mode : values()) {
            if (mode.command != null && mode.command.equals(command)) {
                return mode;
            }
        }
        return NONE;
    }
}
