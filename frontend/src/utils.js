export function formatSquareFeet(value) {
  return `${value.toLocaleString()} sq ft`;
}

export function formatUSD(value) {
  return `$${value.toLocaleString('en-US', { style: 'currency', currency: 'USD' }).slice(1)}`;
}