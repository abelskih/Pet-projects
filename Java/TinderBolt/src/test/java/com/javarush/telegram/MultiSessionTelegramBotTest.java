package com.javarush.telegram;

import org.junit.jupiter.api.Test;
import org.telegram.telegrambots.meta.api.methods.BotApiMethod;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.CallbackQuery;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.MessageEntity;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.User;

import java.io.Serializable;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class MultiSessionTelegramBotTest {

    @Test
    void getCurrentChatId_fromMessage() {
        TestBot bot = new TestBot();
        Update update = updateWithMessage("/start", true, 123L);

        bot.setUpdate(update);

        assertEquals(123L, bot.getCurrentChatId());
    }

    @Test
    void getCurrentChatId_fromCallbackQuery() {
        TestBot bot = new TestBot();
        Update update = updateWithCallback("any", 77L);

        bot.setUpdate(update);

        assertEquals(77L, bot.getCurrentChatId());
    }

    @Test
    void getCurrentChatId_whenNoMessageOrCallback_returnsNull() {
        TestBot bot = new TestBot();

        bot.setUpdate(new Update());

        assertNull(bot.getCurrentChatId());
    }

    @Test
    void getMessageText_whenMessagePresent() {
        TestBot bot = new TestBot();
        Update update = updateWithMessage("hello", false, 1L);

        bot.setUpdate(update);

        assertEquals("hello", bot.getMessageText());
    }

    @Test
    void getMessageText_whenNoMessage_returnsEmptyString() {
        TestBot bot = new TestBot();
        Update update = updateWithCallback("btn", 1L);

        bot.setUpdate(update);

        assertEquals("", bot.getMessageText());
    }

    @Test
    void isMessageCommand_trueWhenCommandEntityPresent() {
        TestBot bot = new TestBot();
        Update update = updateWithMessage("/start", true, 1L);

        bot.setUpdate(update);

        assertTrue(bot.isMessageCommand());
    }

    @Test
    void isMessageCommand_falseWhenNotCommand() {
        TestBot bot = new TestBot();
        Update update = updateWithMessage("hello", false, 1L);

        bot.setUpdate(update);

        assertFalse(bot.isMessageCommand());
    }

    @Test
    void getCallbackQueryButtonKey_returnsData() {
        TestBot bot = new TestBot();
        Update update = updateWithCallback("btn_key", 1L);

        bot.setUpdate(update);

        assertEquals("btn_key", bot.getCallbackQueryButtonKey());
    }

    @Test
    void getCallbackQueryButtonKey_whenNoCallback_returnsEmptyString() {
        TestBot bot = new TestBot();
        Update update = updateWithMessage("hello", false, 1L);

        bot.setUpdate(update);

        assertEquals("", bot.getCallbackQueryButtonKey());
    }

    @Test
    void sendTextMessage_validMarkdown_usesSendMessageApi() {
        TestBot bot = new TestBot();
        Update update = updateWithMessage("hi", false, 456L);

        bot.setUpdate(update);
        bot.sendTextMessage("hello__world");

        assertNotNull(bot.lastSendMessage);
        assertEquals("hello__world", bot.lastSendMessage.getText());
        assertEquals("markdown", bot.lastSendMessage.getParseMode());
        assertEquals("456", bot.lastSendMessage.getChatId());
        assertNull(bot.lastHtmlMessageText);
    }

    @Test
    void sendTextMessage_invalidMarkdown_usesHtmlFallback() {
        TestBot bot = new TestBot();
        Update update = updateWithMessage("hi", false, 456L);

        bot.setUpdate(update);
        bot.sendTextMessage("hello_world");

        assertNull(bot.lastSendMessage);
        assertNotNull(bot.lastHtmlMessageText);
    }

    private static Update updateWithMessage(String text, boolean isCommand, long userId) {
        Update update = new Update();
        Message message = new Message();
        message.setText(text);

        User user = new User();
        user.setId(userId);
        message.setFrom(user);

        if (isCommand) {
            MessageEntity entity = new MessageEntity();
            entity.setType("bot_command");
            entity.setOffset(0);
            entity.setLength(text.length());
            message.setEntities(List.of(entity));
        }

        update.setMessage(message);
        return update;
    }

    private static Update updateWithCallback(String data, long userId) {
        Update update = new Update();
        CallbackQuery callbackQuery = new CallbackQuery();

        User user = new User();
        user.setId(userId);
        callbackQuery.setFrom(user);
        callbackQuery.setData(data);

        update.setCallbackQuery(callbackQuery);
        return update;
    }

    private static class TestBot extends MultiSessionTelegramBot {
        SendMessage lastSendMessage;
        String lastHtmlMessageText;

        TestBot() {
            super("test-bot", "test-token");
        }

        void setUpdate(Update update) {
            onUpdateReceived(update);
        }

        @Override
        public void onUpdateEventReceived(Update updateEvent) {
            // no-op
        }

        @Override
        protected <T extends Serializable, Method extends BotApiMethod<T>> T executeTelegramApiMethod(Method method) {
            if (method instanceof SendMessage sendMessage) {
                this.lastSendMessage = sendMessage;
            }
            return (T) new Message();
        }

        @Override
        public Message sendHtmlMessage(String text) {
            this.lastHtmlMessageText = text;
            return new Message();
        }
    }
}
