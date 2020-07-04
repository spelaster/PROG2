

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.*;
import java.util.Arrays;
import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import java.awt.*;


public class Memo {

    public static final Color PURPLE = new Color(102, 0, 153);

    public static int cX = 75;
    public static int cY = 75;

    private static class Krog {
        int x;
        int y;
        int r = 50;
        Color barva;

        public Krog(int xk, int yk, Color barva_k) {
            this.x = xk;
            this.y = yk;
            this.barva = barva_k;
        }
    }

    static LinkedList<Krog> krogi = new LinkedList<>();
    static LinkedList<Krog> prikaz = new LinkedList<>();
    static LinkedList<Integer> vnos = new LinkedList<>();
    static LinkedList<Krog> resitevList = new LinkedList<>();
    static int[] barve;
    static int pravilnihMest = 0;
    static int pravilnihBarv = 0;
    static int poskus = 0;
    static int tezavnost = 24;
    static int tezavnostRaw = 6;

    private static void dodajKrog(Color barva) {
        Krog nov = new Krog(cX, cY, barva);
        krogi.add(nov);

        cX += 75;
        if (cX > 300) {
            cX = 75;
            cY += 75;
        }
    }

    private static class Panel extends JPanel {

        public Panel() {
            super();
            setBackground(Color.WHITE);
        }

        public void paint(Graphics g) {
            super.paint(g); // klic metode nadrazreda
            Graphics2D graphics = (Graphics2D) g; // pretvarjanje tipov
            graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2

            for (int i = 0; i < krogi.size(); i++) {
                Krog trenutni = krogi.get(i);
                graphics.setColor(trenutni.barva);
                graphics.fillOval(trenutni.x, trenutni.y, trenutni.r, trenutni.r);
            }

            for (int i = 0; i < prikaz.size(); i++) {
                Krog trenutni = prikaz.get(i);
                graphics.setColor(trenutni.barva);
                graphics.fillOval(600 + trenutni.x, trenutni.y-75, trenutni.r, trenutni.r);
                graphics.setColor(Color.BLACK);
                graphics.drawOval(600 + trenutni.x, trenutni.y-75, trenutni.r, trenutni.r);
            }

            for (int i = 0; i < resitevList.size(); i++) {
                Krog trenutni = resitevList.get(i);
                graphics.setColor(trenutni.barva);
                graphics.fillOval(trenutni.x, trenutni.y, trenutni.r, trenutni.r);
            }
        }
    }

    /*
    Računalnik naključno izbere 4 izmed 6 barv
     */
    private static int[] izbira() {

        LinkedList<Integer> barveList = new LinkedList<Integer>();

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

    /*
     Prikaže se pravilna resitev
     */
    private static void izpisiResitev(int[] resitev, JPanel panel) {

        Color[] barve = new Color[4];

        for (int i = 0; i < 4; i++) {
            switch (resitev[i]) {
                case 1:
                    barve[i] = Color.BLUE;
                    break;
                case 2:
                    barve[i] = Color.RED;
                    break;
                case 3:
                    barve[i] = Color.YELLOW;
                    break;
                case 4:
                    barve[i] = Color.GREEN;
                    break;
                case 5:
                    barve[i] = PURPLE;
                    break;
                case 6:
                    barve[i] = Color.ORANGE;
                    break;
            }
            Krog nov = new Krog(75 * (i + 1), 75 * tezavnostRaw + 150, barve[i]);
            resitevList.add(nov);
        }
        panel.repaint();
    }

    private static void primerjavaResitev(int[] barve, JPanel panel) {
        int[] help = new int[4];

        for (int i = 0; i < 4; i++) {
            help[i] = barve[i];
        }

        if (vnos.size() >= 4) {
            for (int i = 0; i < 4; i++) {
                if (vnos.get(i) == help[i]) {
                    pravilnihMest++;
                    vnos.set(i, 0);
                    help[i] = 0;
                }
            }
            for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 4; j++) {
                    if (help[i] != 0 && help[i] == vnos.get(j)) {
                        pravilnihBarv++;
                        help[i] = 0;
                        vnos.set(j, 0);
                    }
                }
            }
            for (int i = 0; i < pravilnihMest; i++) {
                Krog nov = new Krog(i*75, cY, Color.BLACK);
                prikaz.add(nov);
            }
            for (int i = 0; i < pravilnihBarv; i++) {
                Krog nov = new Krog((i + pravilnihMest)*75, cY, Color.WHITE);
                prikaz.add(nov);
            }
            if (pravilnihMest == 4 || poskus >= tezavnost - 1) {
                izpisiResitev(barve, panel);
            }
            panel.repaint();
            vnos.clear();
            pravilnihMest = 0;
            pravilnihBarv = 0;
        }
    }

    private static void novaIgra() {
        krogi.clear();
        prikaz.clear();
        vnos.clear();
        resitevList.clear();
        tezavnost = tezavnostRaw * 4;
        pravilnihMest = 0;
        pravilnihBarv = 0;
        poskus = 0;
        cX = 75;
        cY = 75;
        barve = izbira();
    }

    private static void navodila() {
        JFrame frame = new JFrame("Memo - navodila");
        TextArea area = new TextArea("Računalnik ob začetku igre izbere 4 od 6 različnih barv (modra, rdeča, rumena, zelena, vijolična in oranžna) brez ponavljanja.\n" +
                "Cilj igre je razvozlati barvno šifro.\n" +
                "Glede na izbrano težavnost ima igralec na voljo 5, 6, ali 7 poskusov.\n" +
                "Za vsako pravilno izbrano bravo, se igracu pokaže bel krogec, za bravo, ki je na pravem mestu pa črn krogec.\n" +
                "Igra se konča, ko igralec ugane šifro ali mu zmanjka poskusov.\n", 1, 1, TextArea.SCROLLBARS_NONE);
        Font font = new Font("Verdana", Font.PLAIN, 20);
        area.setFont(font);
        frame.add(area);
        frame.setSize(new Dimension(720, 540)); // nastavimo sirino in dolzino okna
        frame.setResizable(true); // velikost okna lahko spreminjamo
        frame.setVisible(true);
        area.setEditable(false);
    }

    public static void main(String[] args) {
        int x1 = 25;
        int x2 = 0;
        int y1 = 50;
        int y2 = 25;

        barve = izbira();

        JFrame frame = new JFrame("Memo, ugani barve!");
        frame.setSize(new Dimension(1024, 720)); // nastavimo sirino in dolzino okna
        frame.setMinimumSize(new Dimension(1000, 800));
        frame.setResizable(true); // velikost okna lahko spreminjamo

        JPanel panel = new Panel(); // new JPanel();
        frame.add(panel);

        frame.setLayout(new BorderLayout());
        frame.add(panel, BorderLayout.CENTER); // bel panel dodamo v center
        JPanel north = new JPanel();
        frame.add(north, BorderLayout.NORTH); // en panel dodamo na vrh

        /*
        Izbire v menuju.
         */
        JMenuBar mb = new JMenuBar();
        JMenu menu = new JMenu("Meni");
        JMenu tezavnostMenu = new JMenu("Težavnost");
        JMenuItem pravila = new JMenuItem("Pravila");
        JMenuItem igra = new JMenuItem("Nova igra");
        JMenuItem lahka = new JMenuItem("Lahka težavnost");
        JMenuItem srednja = new JMenuItem("Srednja težavnost");
        JMenuItem tezka = new JMenuItem("Težka težavnost");

        menu.add(pravila);
        menu.add(igra);
        menu.add(tezavnostMenu);
        tezavnostMenu.add(lahka);
        tezavnostMenu.add(srednja);
        tezavnostMenu.add(tezka);
        mb.add(menu);

        frame.setJMenuBar(mb);

        pravila.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                navodila();
            }
        });

        igra.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                novaIgra();
                panel.repaint();
            }
        });

        lahka.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                tezavnostRaw = 7;
                novaIgra();
                panel.repaint();
            }
        });

        srednja.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                tezavnostRaw = 6;
                novaIgra();
                panel.repaint();
            }
        });

        tezka.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                tezavnostRaw = 5;
                novaIgra();
                panel.repaint();
            }
        });

        north.add(new JLabel("Izberi barvo: ")); // napis na začetku severnega panela

        JButton button0 = new JButton("Modra"); // dodamo gumb
        button0.setPreferredSize(new Dimension(96, 40));
        button0.setBackground(Color.BLUE);
        button0.setForeground(Color.WHITE);
        button0.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                if (poskus < tezavnost) {
                    dodajKrog(Color.BLUE);
                    panel.repaint();
                    vnos.add(1);
                    primerjavaResitev(barve, panel);
                    poskus++;
                }
            }
        });
        north.add(button0);

        JButton button1 = new JButton("Rdeča"); // dodamo gumb
        button1.setPreferredSize(new Dimension(96, 40));
        button1.setBackground(Color.RED);
        button1.setForeground(Color.WHITE);
        button1.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (poskus < tezavnost) {
                    dodajKrog(Color.RED);
                    panel.repaint();
                    vnos.add(2);
                    primerjavaResitev(barve, panel);
                    poskus++;
                }
            }
        });
        north.add(button1);

        JButton button2 = new JButton("Rumena"); // dodamo gumb
        button2.setPreferredSize(new Dimension(96, 40));
        button2.setBackground(Color.YELLOW);
        button2.setForeground(Color.BLACK);
        button2.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (poskus < tezavnost) {
                    dodajKrog(Color.YELLOW);
                    panel.repaint();
                    vnos.add(3);
                    primerjavaResitev(barve, panel);
                    poskus++;
                }
            }
        });
        north.add(button2);

        JButton button3 = new JButton("Zelena"); // dodamo gumb
        button3.setPreferredSize(new Dimension(96, 40));
        button3.setBackground(Color.GREEN);
        button3.setForeground(Color.BLACK);
        button3.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (poskus < tezavnost) {
                    dodajKrog(Color.GREEN);
                    panel.repaint();
                    vnos.add(4);
                    primerjavaResitev(barve, panel);
                    poskus++;
                }
            }
        });
        north.add(button3);

        JButton button4 = new JButton("Vijolična"); // dodamo gumb
        button4.setPreferredSize(new Dimension(96, 40));
        button4.setBackground(PURPLE);
        button4.setForeground(Color.WHITE);
        button4.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (poskus < tezavnost) {
                    dodajKrog(PURPLE);
                    panel.repaint();
                    vnos.add(5);
                    primerjavaResitev(barve, panel);
                    poskus++;
                }
            }
        });
        north.add(button4);

        JButton button5 = new JButton("Oranžna"); // dodamo gumb
        button5.setPreferredSize(new Dimension(96, 40));
        button5.setBackground(Color.ORANGE);
        button5.setForeground(Color.WHITE);
        button5.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (poskus < tezavnost) {
                    dodajKrog(Color.ORANGE);
                    panel.repaint();
                    vnos.add(6);
                    primerjavaResitev(barve, panel);
                    poskus++;
                }
            }
        });
        north.add(button5);

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
