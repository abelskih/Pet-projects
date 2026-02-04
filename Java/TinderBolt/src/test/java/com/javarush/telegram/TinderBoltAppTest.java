package com.javarush.telegram;

import org.junit.jupiter.api.Test;
import org.telegram.telegrambots.meta.api.objects.CallbackQuery;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.MessageEntity;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.User;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TinderBoltAppTest {

    @Test
    void startCommand_setsMainMode_andShowsScreen() {
        TestApp app = new TestApp();

        app.onUpdateReceived(updateWithMessage("/start", true, 10L));

        assertEquals(DialogMode.MAIN, app.getDialogMode());
        assertEquals("main", app.lastPhotoKey);
        assertNotNull(app.lastTextMessage);
        assertTrue(app.showMainMenuCalled);
    }

    @Test
    void profileFlow_collectsAnswers_andAdvancesQuestions() {
        TestApp app = new TestApp();

        app.onUpdateReceived(updateWithMessage("/profile", true, 10L));
        assertEquals(DialogMode.PROFILE, app.getDialogMode());
        assertEquals(1, app.getQuestionCount());

        app.onUpdateReceived(updateWithMessage("25", false, 10L));
        assertEquals(2, app.getQuestionCount());
        assertEquals("25", app.getUserInfo().age);

        app.onUpdateReceived(updateWithMessage("Developer", false, 10L));
        assertEquals(3, app.getQuestionCount());
        assertEquals("Developer", app.getUserInfo().occupation);
    }

    @Test
    void messageMode_addsToHistoryList() {
        TestApp app = new TestApp();

        app.onUpdateReceived(updateWithMessage("/message", true, 10L));
        assertEquals(DialogMode.MESSAGE, app.getDialogMode());

        app.onUpdateReceived(updateWithMessage("hello there", false, 10L));
        assertEquals(List.of("hello there"), app.getUserMessages());
    }

    @Test
    void timerStartStop_updatesTimerState_andSendsElapsedSeconds() {
        TestApp app = new TestApp();
        app.times.add(1_000L);
        app.times.add(6_000L);

        app.onUpdateReceived(updateWithCallback("start", 10L));
        assertTrue(app.isTimerRunning());

        app.onUpdateReceived(updateWithCallback("stop", 10L));
        assertFalse(app.isTimerRunning());
        assertNotNull(app.lastTextMessage);
        assertTrue(app.lastTextMessage.contains("5"));
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

    private static class TestApp extends TinderBoltApp {
        String lastTextMessage;
        String lastPhotoKey;
        boolean showMainMenuCalled;
        Deque<Long> times = new ArrayDeque<>();

        TestApp() {
            super(new TelegramBotProperties(), new FakeChatService());
        }

        @Override
        public Message sendTextMessage(String text) {
            lastTextMessage = text;
            return new Message();
        }

        @Override
        public Message sendPhotoMessage(String photoKey) {
            lastPhotoKey = photoKey;
            return new Message();
        }

        @Override
        public Message sendTextButtonsMessage(String text, String... buttons) {
            lastTextMessage = text;
            return new Message();
        }

        @Override
        public void showMainMenu(String... commands) {
            showMainMenuCalled = true;
        }

        @Override
        protected void editButtonsToOnlyStop(Update update) {
            // no-op in tests
        }

        @Override
        protected void hideButtons(Update update) {
            // no-op in tests
        }

        @Override
        protected void answerCallback(Update update) {
            // no-op in tests
        }

        @Override
        protected long nowMillis() {
            return times.isEmpty() ? 0L : times.removeFirst();
        }
    }

    private static class FakeChatService implements ChatService {
        @Override
        public String sendMessage(String prompt, String question) {
            return "ok";
        }

        @Override
        public void setPrompt(String prompt) {
            // no-op
        }

        @Override
        public String addMessage(String question) {
            return "ok";
        }
    }
}
