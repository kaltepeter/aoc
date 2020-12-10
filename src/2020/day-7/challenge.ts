import { match } from 'ramda';

export interface IRule {
  [key: string]: string[];
}

export type Rule = [string, string];

export interface BNode {
  name: string;
  counted: boolean;
  children: BNode[];
}

export interface BNodeList {
  [key: string]: BNode;
}

/**
 * Filter list of rules to bags that hold a certain color
 * @param rules List of rules
 * @param bagToFind string of bag name
 */
const findBagsThatHoldAColor = (rules: Rule[], bagToFind: string) =>
  rules.filter((r) => match(new RegExp(bagToFind), r[1]).length > 0);

/**
 * Filter rulesList to get bags that contain no bags
 * @param rules List of rules
 */
const stopBags = (rules: Rule[]) =>
  rules.filter((r: Rule) => match(/no other bags/, r[1]).length > 0);

const getBagsForChildren = (bagList: string) =>
  bagList
    .split(',')
    .map((b) => b.trim().replace(/[0-9]+ ([a-zA-Z\s]+) bags?[,\.]?/, '$1'));

const getNode = (listOfBags: BNodeList, name: string): BNode => {
  if (!listOfBags[name]) {
    listOfBags[name] = {
      counted: false,
      name,
      children: [],
    };
  }
  return listOfBags[name];
};

const walkListOfBags = (rules: Rule[]): BNodeList => {
  const bagTree: BNodeList = {};
  rules.map((r: Rule) => {
    if (match(/no other bags/, r[1]).length > 0) {
      return;
    }
    const node = getNode(bagTree, r[0]);

    let childBags = getBagsForChildren(r[1]);
    do {
      const bag = childBags.pop();
      if (bag) {
        node.children.push(getNode(bagTree, bag));
      }
    } while (childBags.length > 0);
  });
  return bagTree;
};

const countBags = (bagList: BNode[], startCount = 0): number =>
  bagList.reduce((acc, b) => {
    if (!b.counted) {
      acc++;
    }
    b.counted = true;
    return acc;
  }, startCount);

const getListOfBagsThatHoldAColor = (bagName: string, bagTree: BNodeList) => {
  let total = 0;

  const walkBags = (node: BNode, bagList: BNode[] = []): number => {
    if (node.name === bagName) {
      total += countBags(bagList);
      return total;
    }
    bagList.push(node);
    node.children.reduce((acc, n) => (acc = acc + walkBags(n, bagList)), total);
    bagList.pop();
    return total;
  };

  for (const bag of Object.values(bagTree)) {
    walkBags(bag);
  }
  return total;
};

export {
  findBagsThatHoldAColor,
  getListOfBagsThatHoldAColor,
  getBagsForChildren,
  walkListOfBags,
  stopBags,
  countBags,
};
