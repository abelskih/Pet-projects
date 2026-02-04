package com.javarush.telegram;

public interface ChatService {
    String sendMessage(String prompt, String question);
    void setPrompt(String prompt);
    String addMessage(String question);
}
