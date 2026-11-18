export interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
}

export type SortKey = "name" | "price";

const compare = (a: string | number, b: string | number): number =>
  typeof a === "number" && typeof b === "number"
    ? a - b
    : String(a).localeCompare(String(b));

export function stableSortBy(
  items: readonly Product[],
  key: SortKey,
  dir: 1 | -1 = 1
): Product[] {
  return items
    .map((value, index) => ({ value, index }))
    .sort((a, b) => compare(a.value[key], b.value[key]) * dir || a.index - b.index)
    .map((entry) => entry.value);
}

export function byCategory(items: readonly Product[], category: string): Product[] {
  return category === "All" ? [...items] : items.filter((p) => p.category === category);
}

export function cartTotal(
  items: readonly Product[],
  cart: Readonly<Record<number, number>>
): number {
  return items.reduce((sum, p) => sum + p.price * (cart[p.id] ?? 0), 0);
}
