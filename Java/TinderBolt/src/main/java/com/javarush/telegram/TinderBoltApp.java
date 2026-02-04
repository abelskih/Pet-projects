package com.javarush.telegram;

import com.javarush.telegram.DialogMode;
import com.javarush.telegram.MultiSessionTelegramBot;
import com.javarush.telegram.UserInfo;
import jakarta.annotation.PostConstruct;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.api.methods.AnswerCallbackQuery;
import org.telegram.telegrambots.meta.api.methods.updatingmessages.EditMessageReplyMarkup;
import org.telegram.telegrambots.meta.api.objects.*;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import com.javarush.telegram.TelegramBotProperties;

import java.util.ArrayList;

@SpringBootApplication
@ConfigurationPropertiesScan
public class TinderBoltApp extends MultiSessionTelegramBot {

    private final ChatService chatService;
    private DialogMode dialogMode = DialogMode.NONE;
    private String gptPrompt;
    private ArrayList<String> list = new ArrayList();
    private UserInfo userInfo;
    private int questionCount;

    //для таймера
    private boolean timerRunning = false;
    private long timerStartMillis = 0L;

    public TinderBoltApp(TelegramBotProperties props, ChatService chatService) {
        super(props.getUsername(), props.getToken());
        this.chatService = chatService;
    }

    @PostConstruct
    public void register() throws TelegramApiException {
        TelegramBotsApi api = new TelegramBotsApi(DefaultBotSession.class);
        api.registerBot(this);
    }

    @Override
    public void onUpdateEventReceived(Update update) {

        if (update.hasCallbackQuery()) {
            String data = update.getCallbackQuery().getData();
            if (data == null || data.isBlank()) return;
            handleCallback(update, data);
            return;
        }

        String message = getMessageText();
        if (message == null || message.isBlank()) return;
        if (handleCommand(message)) return;
        if (handleDialog(message)) return;
        handleFallback(message);
    }

    private boolean handleCommand(String message) {

        DialogMode mode = DialogMode.fromCommand(message);
        if (mode == DialogMode.NONE) {
            return false;
        }
        switch (mode) {
            case MAIN -> {
                onStart();
                return true;
            }
            case GPT -> {
                onGpt();
                return true;
            }
            case DATE -> {
                onDate();
                return true;
            }
            case MESSAGE -> {
                onMessage();
                return true;
            }
            case PROFILE -> {
                onProfile();
                return true;
            }
            case OPENER -> {
                onOpener();
                return true;
            }
            default -> {
                return false;
            }
        }
    }

    private boolean handleDialog(String message) {
        if (dialogMode == DialogMode.GPT) {
            Message msg = sendTextMessage("ChatGPT думает ...");
            String answer = chatService.sendMessage(gptPrompt, message);
            updateTextMessage(msg, answer);
            return true;
        }
        if (dialogMode == DialogMode.DATE) {
            Message msg = sendTextMessage("Печатает ...");
            String answer = chatService.addMessage(message);
            updateTextMessage(msg, answer);
            return true;
        }
        if (dialogMode == DialogMode.MESSAGE) {
            list.add(message);
            return true;
        }
        if (dialogMode == DialogMode.PROFILE) {
            switch (questionCount)
            {
                case 1:
                    userInfo.age = message;
                    questionCount=2;
                    sendTextMessage("Кем вы работаете?");
                    return true;
                case 2:
                    userInfo.occupation = message;
                    questionCount=3;
                    sendTextMessage("Какое у вас хобби?");
                    return true;
                case 3:
                    userInfo.hobby = message;
                    questionCount=4;
                    sendTextMessage("Что вам не нравится в людях?");
                    return true;
                case 4:
                    userInfo.annoys=message;
                    questionCount=5;
                    sendTextMessage("Какая цель знакомства?");
                    return true;
                case 5:
                    userInfo.goals=message;
                    String aboutMySelf = userInfo.toString();
                    Message msg = sendTextMessage("ChatGPT думает ...");
                    String answer = chatService.sendMessage(gptPrompt, aboutMySelf);
                    updateTextMessage(msg, answer);
                    return true;
            }
        }
        if (dialogMode == DialogMode.OPENER) {

            switch (questionCount)
            {
                case 1:
                    userInfo.name = message;
                    questionCount=2;
                    sendTextMessage("Сколько ей лет?");
                    return true;
                case 2:
                    userInfo.age = message;
                    questionCount=3;
                    sendTextMessage("Какое у нее хобби?");
                    return true;
                case 3:
                    userInfo.hobby = message;
                    questionCount=4;
                    sendTextMessage("Кем она работает?");
                    return true;
                case 4:
                    userInfo.occupation=message;
                    questionCount=5;
                    sendTextMessage("Какая цель знакомства?");
                    return true;
                case 5:
                    userInfo.goals=message;
                    String aboutMySelf = userInfo.toString();
                    Message msg = sendTextMessage("ChatGPT думает ...");
                    String answer = chatService.sendMessage(gptPrompt, aboutMySelf);
                    updateTextMessage(msg, answer);
                    return true;
            }

        }
        return false;
    }

    private void onStart() {
        dialogMode = DialogMode.MAIN;

        showMainMenu(
                "главное меню бота", DialogMode.MAIN.getCommand(),
                "генерация Tinder-профля 😎", DialogMode.PROFILE.getCommand(),
                "сообщение для знакомства 🥰", DialogMode.OPENER.getCommand(),
                "переписка от вашего имени 😈", DialogMode.MESSAGE.getCommand(),
                "переписка со звездами 🔥", DialogMode.DATE.getCommand(),
                "задать вопрос чату GPT 🧠", DialogMode.GPT.getCommand()
        );
        showScreen(dialogMode.name().toLowerCase());
    }

    private void onGpt() {
        dialogMode = DialogMode.GPT;
        gptPrompt = loadPrompt(dialogMode.name().toLowerCase());
        showScreen(dialogMode.name().toLowerCase());
    }

    private void onDate() {
        dialogMode = DialogMode.DATE;
        showScreen(dialogMode.name().toLowerCase());
        sendTextButtonsMessage("Выберите кого вы хотите пригласиь на свидание:",
                "Ариана Гранде","date_grande",
                "Марго Робби","date_robbie",
                "Зендея","date_zendaya",
                "Райан Гослинг","date_gosling",
                "Том Харди","date_hardy"
                );
    }

    private void onMessage() {
        dialogMode = DialogMode.MESSAGE;
        showScreen(dialogMode.name().toLowerCase());
        sendTextButtonsMessage("Как будешь готов нажимай:",
                "Следующее сообщение","message_next",
                "Пригласить на свидание","message_date"
        );
    }

    private void onProfile() {
        dialogMode = DialogMode.PROFILE;
        gptPrompt = loadPrompt(dialogMode.name().toLowerCase());
        userInfo = new UserInfo();
        questionCount=1;
        showScreen(dialogMode.name().toLowerCase());
        sendTextMessage("Сколько вам лет?");
    }

    private void onOpener() {
        dialogMode = DialogMode.OPENER;
        gptPrompt = loadPrompt(dialogMode.name().toLowerCase());
        userInfo = new UserInfo();
        questionCount=1;
        showScreen(dialogMode.name().toLowerCase());
        sendTextMessage("Какое имя собеседника?");
    }

    protected void showScreen(String key) {
        sendPhotoMessage(key);
        sendTextMessage(loadMessage(key));
    }

    private void handleFallback(String message) {
        sendTextMessage("*Привет!* _Hello!_");
        sendTextMessage("Вы написали: " + message);
        sendTextButtonsMessage("Выберите режим работы:",
                "Старт", "start",
                "Стоп", "stop");
    }

    private void handleCallback(Update update, String data) {
        switch (data) {
            //сделал тут запуск таймера по кнопке "Старт" и остановке по кнопке "Стоп"
            case "start" -> onTimerStart(update);
            case "stop" -> onTimerStop(update);
            default -> {
                if (data.startsWith("date_")) {
                    onDateSelected(update, data);
                    return;
                }
                if (data.startsWith("message_")) {
                    onMessageAction(update, data);
                    return;
                }
            }
        }
    }
    protected void onDateSelected(Update update, String key) {
        answerCallback(update);
        sendPhotoMessage(key);
        chatService.setPrompt(loadPrompt(key));
        sendTextMessage("Отличный выбор! \nТвоя задача пригласить собеседника за 5 сообщений.");
    }

    protected void onMessageAction(Update update, String key) {
        answerCallback(update);
        String prompt = loadPrompt(key);
        String userChatHistory = String.join("\n\n", list);
        Message msg = sendTextMessage("ChatGPT думает ...");
        String answer = chatService.sendMessage(prompt, userChatHistory);
        updateTextMessage(msg, answer);
    }


    protected void onTimerStart(Update update) {

        if (!timerRunning) {
            timerRunning = true;
            timerStartMillis = nowMillis();
        }
        editButtonsToOnlyStop(update);

        answerCallback(update);
    }

    protected void onTimerStop(Update update) {

        hideButtons(update);

        if (timerRunning) {
            long elapsedMillis = nowMillis() - timerStartMillis;
            long elapsedSeconds = elapsedMillis / 1000;

            timerRunning = false;
            timerStartMillis = 0L;

            sendTextMessage("⏱ Таймер остановлен. Прошло секунд: " + elapsedSeconds);
        }

        answerCallback(update);
    }

    protected void editButtonsToOnlyStop(Update update) {
        CallbackQuery cq = update.getCallbackQuery();
        Message msg = extractMessage(cq);

        if (msg == null) return;

        InlineKeyboardButton stopButton = new InlineKeyboardButton("Стоп");
        stopButton.setCallbackData("stop");

        InlineKeyboardMarkup markup = new InlineKeyboardMarkup(
                java.util.List.of(
                        java.util.List.of(stopButton)
                )
        );

        EditMessageReplyMarkup edit = new EditMessageReplyMarkup();
        edit.setChatId(msg.getChatId());
        edit.setMessageId(msg.getMessageId());
        edit.setReplyMarkup(markup);

        try { execute(edit);
        } catch (TelegramApiException e) {
            throw new RuntimeException(e);
        }
    }

    protected Message extractMessage(CallbackQuery cq) {
        if (cq.getMessage() instanceof Message msg) {
            return msg;
        }
        return null;
    }

    protected void hideButtons(Update update) {
        CallbackQuery cq = update.getCallbackQuery();
        Message msg = extractMessage(cq);
        if (msg == null) return;
        EditMessageReplyMarkup edit = new EditMessageReplyMarkup();
        edit.setChatId(msg.getChatId());
        edit.setMessageId(msg.getMessageId());
        edit.setReplyMarkup(null); // это убирает inline клавиатуру
        try {
            execute(edit);
        } catch (TelegramApiException e) {
            throw new RuntimeException(e);
        }
    }

    protected void answerCallback(Update update) {
        try {
            execute(new AnswerCallbackQuery(update.getCallbackQuery().getId()));
        } catch (TelegramApiException e) {
            System.out.println(e.getMessage());
        }
    }

    protected long nowMillis() {
        return System.currentTimeMillis();
    }

    protected DialogMode getDialogMode() {
        return dialogMode;
    }

    protected int getQuestionCount() {
        return questionCount;
    }

    protected UserInfo getUserInfo() {
        return userInfo;
    }

    protected ArrayList<String> getUserMessages() {
        return list;
    }

    protected boolean isTimerRunning() {
        return timerRunning;
    }

    public static void main(String[] args) {
        SpringApplication.run(TinderBoltApp.class, args);
    }
}
