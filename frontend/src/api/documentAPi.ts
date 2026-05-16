import { mockDocuments } from '../pages/Document/mockDocuments';
import type { IntegratedDocument } from '../pages/Document/types';

const getIntegratedDocuments = async (): Promise<IntegratedDocument[]> => {
  return Promise.resolve(mockDocuments);
};

export { getIntegratedDocuments };
export default getIntegratedDocuments;