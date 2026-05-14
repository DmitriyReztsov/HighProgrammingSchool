package ooap.datastructures;

import org.apache.commons.lang3.StringUtils;
import java.time.LocalDate;
import java.util.Set;

public class App {
    // BEGIN (write your solution here)
    public static void gogo() {
        System.out.println("It works");
    }
    // END
    
    public static String sayHurrayThreeTimes() {
        return "hurray! ".repeat(3).trim();
    }

    public static String truncate(String text, int length) {
        // BEGIN (write your solution here)
        return String.format("%s...", text.substring(0, length));
        // END
    }

    public static String getHiddenCard(String cardNumber, int starsNum) {
        return String.format("%s%s", "*".repeat(starsNum), cardNumber.substring(12));
    }

    public static String getHiddenCard(String cardNumber) {
        return App.getHiddenCard(cardNumber, 4);
    }

    public static boolean isPensioner(int age) {
        return age >= 60;
    }

    public static boolean isPalindrome(String str) {
        String reversedStr = StringUtils.reverse(str);
        return str.equalsIgnoreCase(reversedStr);
    }

    public static boolean isInternationalPhone(String phone) {
        return phone.charAt(0) == '+';
    }

    public static boolean isLeapYear(int year) {
        return year % 400 == 0 || (year % 4 == 0 && year % 100 != 0);
    }

    public static boolean notToday(String dateStr) {
        LocalDate today = LocalDate.now();
        String todayStr = today.toString();

        return !dateStr.equals(todayStr);
    }

    public static String getSentenceTone(String sentence) {
        if (sentence.toUpperCase().equals(sentence)) {
            return "scream";
        }
        return "normal";
    }

    public static String normalizeUrl(String url) {
        String prefix = "https://";

        if (url.startsWith(prefix)) {
            return url;
        }

        return prefix + url;
    }

    public static String whoIsThisHouseToStarks(String family) {
        Set<String> friends = Set.of("Karstark", "Tally");
        Set<String> enemies = Set.of("Lannister", "Frey");

        if (friends.contains(family)) {
            return "friend";
        } else if (enemies.contains(family)) {
            return "enemy";
        }
        return "neutral";
    }

    public static String convertString(String str) {
        if (str.equals("")) {
            return "";
        }

        return Character.isUpperCase(str.charAt(0)) ? str : StringUtils.reverse(str);
    }

    public static String getNumberExplanation(int number) {
        switch (number) {
            case 666:
                return "devil number";
            case 42:
                return "answer for everything";
            case 7:
                return "prime number";
            default:
                return "just a number";
        }
    }

    public static int multiplyNumbersFromRange(int start, int end) {
        var result = 1;
        while (start <= end) {
            result *= start;
            start += 1;
        }
        return result;
    }

    public static String joinNumbersFromRange(int start, int end) {
        String result = "";

        while (start <= end) {
            result += start;
            start += 1;
        }
        return result;
    }

    public static String filterString(String text, char toRemove) {
        var i = 0;
        var result = "";

        while (i < text.length()) {
            result += text.charAt(i) == toRemove ? "" : text.charAt(i);
            i++;
        }
        return result;
    }

    public static String makeItFunny(String text, int indToChange) {
        var i = 0;
        var result = "";

        while (i < text.length()) {
            result += (i + 1) % indToChange == 0 ? Character.toUpperCase(text.charAt(i)) : text.charAt(i);
            i++;
        }
        return result;
    }

    public static boolean hasChar(String text, char c) {
        var i = 0;

        while (i < text.length()) {
            if (text.charAt(i) == c) {
                return true;
            }
            i++;
        }
        return false;
    }

    public static String encrypt(String text) {
        var result = "";

        if (text.length() < 2) {
            return text;
        }

        for (var i = 0; i < text.length(); i += 2) {
            result += i+1 == text.length() ? text.charAt(i) : String.valueOf(text.charAt(i+1)) + String.valueOf(text.charAt(i));
            System.out.println(result);
        }
        return result;
    }

    public static void main(String[] args) {
        assert App.isPalindrome("asddsa"): "palindreme";

        assert !App.isLeapYear(2018): "false";
        assert !App.isLeapYear(2017): "false";
        assert App.isLeapYear(2016): "true";
        // assert false;  // Remove this - it always fails

        assert App.notToday("2012-11-25"): "should be true";
        // assert App.notToday("2013-11-25"): "should be true";
        // assert App.notToday("2013-09-01"): "should be true";

        assert App.getSentenceTone("Hello").equals("normal"): "\"Hello\" is normal";
        assert App.getSentenceTone("WOW").equals("scream"): "\"WOW\" is scream";

        assert App.normalizeUrl("google.com").equals("https://google.com"): "\"google.com\" -> \"https://google.com\", got " + App.normalizeUrl("google.com");
        assert App.normalizeUrl("https://ai.fi").equals("https://ai.fi"): "https://ai.fi -> https://ai.fi";

        assert App.whoIsThisHouseToStarks("Karstark").equals("friend"): "Karstark is friend, got " + App.whoIsThisHouseToStarks("Karstark");
        assert App.whoIsThisHouseToStarks("Frey").equals("enemy");
        assert App.whoIsThisHouseToStarks("Joar").equals("neutral");
        assert App.whoIsThisHouseToStarks("Ivanov").equals("neutral");

        assert App.convertString("Hello").equals("Hello");
        assert App.convertString("hello").equals("olleh");
        assert App.convertString("").equals("");

        assert App.getNumberExplanation(8).equals("just a number");
        assert App.getNumberExplanation(666).equals("devil number");
        assert App.getNumberExplanation(42).equals("answer for everything");
        assert App.getNumberExplanation(7).equals("prime number");

        assert App.multiplyNumbersFromRange(1, 5) == 120;
        assert App.multiplyNumbersFromRange(2, 3) == 6;
        assert App.multiplyNumbersFromRange(6, 6) == 6;

        assert App.joinNumbersFromRange(1, 1).equals("1");
        assert App.joinNumbersFromRange(2, 3).equals("23");
        assert App.joinNumbersFromRange(5, 10).equals("5678910");

        var str = "If I look back I am lost";
        assert App.filterString(str, 'I').equals("f  look back  am lost");
        assert App.filterString(str, 'o').equals("If I lk back I am lst");

        var text = "I never look back";
        // Каждый третий элемент
        assert App.makeItFunny(text, 3).equals("I NevEr LooK bAck");

        assert App.hasChar("Renly", 'R'); // true
        assert !App.hasChar("Renly", 'r'); // false
        assert App.hasChar("Tommy", 'm'); // true
        assert !App.hasChar("Tommy", 'd'); // false
        
        assert App.encrypt("move").equals("omev"): "---> " + App.encrypt("move");
        assert App.encrypt("attack").equals("taatkc");
        // Если число символов нечётное,
        // то последний символ остается на своем месте
        assert App.encrypt("go!").equals("og!");

        System.out.println("Assertion ok");
    }
}