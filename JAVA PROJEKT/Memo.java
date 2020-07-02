import javax.swing.*;
import java.util.*;
import java.awt.*;
import java.util.Arrays;

public class Memo {

    //Računalnik naključno izbere 4 izmed 6 barv
    private static int[] izbira() {

        LinkedList<Integer> barveList= new LinkedList<Integer>();

        for (int i = 1; i <= 6; i++) {
            barveList.add(i);
        }

        Collections.shuffle(barveList);

        int[] barve = new int[4];
        for (int i = 0; i < barve.length; i++) {
            barve[i] = barveList.get(i);
        }
        return  barve;
    }


    public static void main(String[] args) {
        int x1 = 25;
        int x2 = 0;
        int y1 = 50;
        int y2 = 25;

        int poskus = 0;
        int tezavnost = 24;
        int tezavnostRaw = 6;
        Color barva = new Color(0, 0, 0);

        int[] barve = izbira();
        int[] vnos = new int[4];
        int[] prikaz = new int[4];
        int pravilnoMestoBarva = 0;
        int pravilnaBarva = 0;

        // Uporabniško okno
        JFrame okvir = new JFrame("Memo, ugani barve!");
        okvir.pack();
        okvir.setVisible(true);

        System.out.println(Arrays.toString(barve));
    }
}
