const byType = items.reduce((groups, item) => {
  (groups[item.type] ??= []).push(item);
  return groups;
}, {});
