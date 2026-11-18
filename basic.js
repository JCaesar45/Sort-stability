function stableSort(arr) {
  return arr
    .map((item, index) => ({ item, index }))
    .sort((a, b) => {
      if (a.item[1] < b.item[1]) return -1;
      if (a.item[1] > b.item[1]) return 1;
      return a.index - b.index; // tie-breaker keeps original order
    })
    .map(({ item }) => item);
}
