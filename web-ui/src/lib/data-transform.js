const transformScheduleToText = (sched=[]) => {
  const mapped = sched.map(curr => {
    let str = curr.operation_type.toLowerCase()[0];

    str += curr.transaction_id;

    if (curr.data_item) {
      str += `[${curr.data_item}]`;
    }

    return str;
  });

  return mapped.join(' ');
};

export {
  transformScheduleToText
}
