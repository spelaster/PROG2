//package si.lj.uni.fmf.pmat.pro2;


import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class Vizualizacija {
	
	public static Point ball = new Point();
	
	public static void main(String[] args) {
		JFrame frame = new JFrame("Memo");
		frame.setSize(new Dimension(1024, 720)); // nastavimo sirino in dolzino okna
		frame.setMinimumSize(new Dimension(800, 600));
		frame.setResizable(true); // velikost okna lahko spreminjamo
		
		JPanel panel = new Panel(); // new JPanel();
		// panel.setBackground(Color.WHITE);
		frame.add(panel);
		
		frame.setLayout(new BorderLayout());
		frame.add(panel, BorderLayout.CENTER); // bel panel dodamo v center
		JPanel north = new JPanel();
		frame.add(north, BorderLayout.NORTH); // en panel dodamo na vrh
		JPanel south = new JPanel();
		frame.add(south, BorderLayout.SOUTH); // in en panel na dno
		
		north.add(new JLabel("Izberi barvo: ")); // napis na začetku severnega panela

		
		
		JButton button0 = new JButton("Modra"); // dodamo gumb
		button0.setPreferredSize(new Dimension(96, 40));
		button0.setBackground(Color.BLUE);
		button0.setForeground(Color.WHITE);
		button0.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				ball = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
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
				ball = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
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
				ball = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
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
				ball = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
			}
		});
		north.add(button3);
		
		JButton button4 = new JButton("Vijolična"); // dodamo gumb
		button4.setPreferredSize(new Dimension(96, 40));
		button4.setBackground(Color.MAGENTA);
		button4.setForeground(Color.WHITE);
		button4.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				ball = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
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
				ball = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
			}
		});
		north.add(button5);
		
		
				
		south.setLayout(new GridLayout(3, 1)); // južnni panel razporedimo v tri vrstice in en stolpec
		for (int i = 0; i < 3; i++) {
			float rgb = (i + 1) / 4.0f; 
			Color color = new Color(rgb, rgb, rgb); // odtenki sive (če so vse tri enake, je to siva)
			JPanel subsouth = new JPanel();
			subsouth.setBackground(color);
			south.add(subsouth);
		}
		
		
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
		
		
	}
	
}

@SuppressWarnings("serial")
class Panel extends JPanel {

	public Panel() {
		super();
		setBackground(Color.WHITE);
	}

	@Override
	public void paint(Graphics g) {
		super.paint(g); // klic metode nadrazreda
		Graphics2D graphics = (Graphics2D)g; // pretvarjanje tipov
		int indent = 65; // pomožne spremenljivke
		int polmer = 50;
		
		int x = 4*indent, y = indent; // narišemo prvi krog
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2
		graphics.fillOval(x, y, polmer, polmer);
		
		x += indent; // narišemo drugi krog
		graphics.setColor(Color.YELLOW);
		graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2
		graphics.fillOval(x, y, polmer, polmer);
		
		x += indent; // narišemo tretji krog
		graphics.setColor(Color.YELLOW);
		graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2
		graphics.fillOval(x, y, polmer, polmer);
		
		x += indent; // narišemo četrti krog
		graphics.setColor(Color.YELLOW);
		graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2
		graphics.fillOval(x, y, polmer, polmer);
		
		x = 4*indent; y += indent; // narišemo korg pod prvim (druga vrstica)
		graphics.setColor(Color.RED);
		graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2
		graphics.fillOval(x, y, polmer, polmer);
		
		x += indent; // narišemo drugi krog v drugi vrstici
		graphics.setColor(Color.YELLOW);
		graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2
		graphics.fillOval(x, y, polmer, polmer);
		
		x += indent; // narišemo tretji krog v drugi vrstici
		graphics.setColor(Color.YELLOW);
		graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2
		graphics.fillOval(x, y, polmer, polmer);
		
		x += indent; // narišemo četrti krog v drugi vrstici
		graphics.setColor(Color.YELLOW);
		graphics.setStroke(new BasicStroke(2.0f)); // čopič debeline 2
		graphics.fillOval(x, y, polmer, polmer);
		
		
		
	}

}

