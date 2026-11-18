import java.util.List;

public class OrderValidator {
    record Line(int id, int qty, int unitPrice) {}

    static final double TAX_RATE = 0.07;

    static long subtotal(List<Line> lines) {
        long sum = 0;
        for (Line line : lines) {
            if (line.qty() < 1 || line.unitPrice() < 0) {
                throw new IllegalArgumentException("Invalid line " + line.id());
            }
            sum += (long) line.qty() * line.unitPrice();
        }
        return sum;
    }

    static boolean validEmail(String email) {
        return email != null && email.matches("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$");
    }

    public static void main(String[] args) {
        List<Line> cart = List.of(new Line(1, 1, 4800), new Line(3, 2, 950));
        long sub = subtotal(cart);
        double tax = Math.round(sub * TAX_RATE * 100) / 100.0;
        System.out.printf("Subtotal: $%d%nTax: $%.2f%nTotal: $%.2f%n", sub, tax, sub + tax);
        System.out.println("Email ok: " + validEmail("client@example.com"));
    }
}
