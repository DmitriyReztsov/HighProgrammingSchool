package ooap.datastructures.Java_cli_5;

import java.util.Arrays;

import ooap.datastructures.Java_cli_5.SwordsMan;


public class CivEmulate {
	
    public static void main(String[] args) {
        SwordsMan sm = new SwordsMan();
        try (Scanner scanner = new Scanner(System.in)) {
            
            while (true) {
                System.out.print("Введите параметры атаки (или 'exit' для выхода): ");
                String paramsAttack = scanner.nextLine();

                if (paramsAttack.equals("exit")) {
                    System.out.println("Программа завершена.");
                    break;
                }

                String[] parts = paramsAttack.split(" ");
                System.out.println("Parts: " + Arrays.toString(parts));

                if (parts.length == 1) {
                    try {
                        int attackParam = Integer.parseInt(paramsAttack);
                        sm.attack(attackParam);
                    } catch (NumberFormatException e) {
                        sm.attack(paramsAttack);
                    }
                } else if (parts.length == 2) {
                    // упрощение валидации, педполагаем, что ввод валидный
                    sm.attack(Integer.parseInt(parts[0]), Integer.parseInt(parts[1]));
                }
            }
        } // Scanner автоматически закроется здесь
    }
}
