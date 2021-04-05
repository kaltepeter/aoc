const divisor = 20201227;
const subject = 7;

const findLoop = (publicKey: number) => {
  let retval = 1;
  let loopSize = 0;
  do {
    retval = (retval * subject) % divisor;
    loopSize++;
  } while (retval !== publicKey);
  return loopSize;
};

const getEncryptionKey = (publicKey: number, loopSize: number) => {
  let encryptionKey = 1;
  for (let i = 0; i < loopSize; i++) {
    encryptionKey = (encryptionKey * publicKey) % divisor;
  }
  return encryptionKey;
};

export { findLoop, getEncryptionKey };
