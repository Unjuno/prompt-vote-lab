const output = document.querySelector('#demo-output');
const button = document.querySelector('#demo-button');

const labels = [
  'Hit: expectation matched the result',
  'Partial: useful but incomplete',
  'Misread: the agent misunderstood the prompt',
  'Overbuild: the agent added too much',
  'Underbuild: the result was too weak',
  'Rule conflict: the prompt conflicted with constraints',
  'Unsafe: the result violated a safety rule',
  'Rejected: the PR should not be merged'
];

button?.addEventListener('click', () => {
  if (!output) return;
  output.textContent = labels.join(' / ');
});
