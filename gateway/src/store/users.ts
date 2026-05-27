export interface TestUser {
  userId: string;
  userName: string;
  password: string;
}

const users = new Map<string, TestUser>();

export const DEFAULT_TEST_USER_ID = '5001185';

const defaults: TestUser[] = [
  { userId: DEFAULT_TEST_USER_ID, userName: '测试用户', password: '123456' },
  { userId: 'user001', userName: '张三', password: 'test123' },
  { userId: 'user002', userName: '李四', password: 'test123' },
  { userId: 'user003', userName: '王五', password: 'test123' },
];

for (const user of defaults) {
  users.set(user.userId, user);
}

export function findByCredentials(userId: string, password: string): TestUser | undefined {
  const user = users.get(userId);
  if (user && user.password === password) {
    return user;
  }
  return undefined;
}

export function findById(userId: string): TestUser | undefined {
  return users.get(userId);
}

export function getDefaultUser(): TestUser {
  return users.get(DEFAULT_TEST_USER_ID)!;
}

export type SafeUser = Omit<TestUser, 'password'>;

export function listAll(): SafeUser[] {
  return Array.from(users.values()).map(({ password: _password, ...rest }) => rest);
}

export function add(user: TestUser): void {
  users.set(user.userId, user);
}

export function remove(userId: string): boolean {
  return users.delete(userId);
}
