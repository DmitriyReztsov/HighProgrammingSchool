package ooap.datastructures;

import java.time.LocalDate;
import java.time.Month;
import java.time.temporal.ChronoUnit;

public class Try {
    public static void main(String[] args) {
        // BEGIN (write your solution here)
        // System.out.println(String.format("%s%s", Character.toUpperCase(name.charAt(0)), name.substring(1).toLowerCase()));
        // END

        // System.out.println((int)(Math.random() * 10));

        var emoji = "-(";
        // BEGIN (write your solution here)
        String smile = ":" + emoji.replace("(", ")");
        System.out.println(smile);
        // END
    }
}