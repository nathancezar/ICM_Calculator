__author__ = 'Equipe-ECV'

from database import connection
from database.models import pos_processing_result_model, contract_model, highway_model
from database.models.result_model import Result
from database.models.icm_model import Icm


class Controller():
    def __init__(self, args):
        self._args = args
        connection.database.connect()

    def close(self):
        """
            Close database connection
        """
        connection.database.close()

    def insertIcm(self, calculatedICM):
        """
            Insert ICM
        """
        with connection.database.atomic() as transaction:
            try:
                connection.database.transaction()
                Icm.create(
                    highway_id=calculatedICM["highway"],
                    km=calculatedICM["km"],
                    direction=calculatedICM["direction"],
                    pothole=calculatedICM["pothole"],
                    repair=calculatedICM["repair"],
                    crack=calculatedICM["crack"],
                    clearing=calculatedICM["clearing"],
                    signal=calculatedICM["signal"],
                    drainage=calculatedICM["drainage"],
                    icp=calculatedICM["ICP"],
                    icc=calculatedICM["ICC"],
                    icm=calculatedICM["ICM"]
                )
                connection.database.commit()
            except KeyboardInterrupt:
                transaction.rollback()
                raise
            except Exception:
                transaction.rollback()
                raise

    def getResults(self, highway, direction):
        """
            Return the results of a highway
        """
        try:
            results = pos_processing_result_model.getResultsByHighway(highway, direction)
            res = []

            for result in results:
                res.append({
                    "item": result.item,
                    "total": result.total,
                    "Km_Calc": result.Km_Calc
                })
            return res
        except Exception as ex:
            raise ex

    def getContract(self, id):
        try:
            contract = contract_model.getContractById(id)
            if contract is not None:
                return contract.id
            else :
                return None

        except Exception as ex:
            raise ex

    def getHighway(self, id):
        try:
            highway = highway_model.getHighwayById(id)
            if highway is not None:
                return highway.id
            else:
                return None

        except Exception as ex:
            raise ex

    def verifyContractAndHighway(self, contractId, highwayId):
        highway = self.getHighway(highwayId)
        contract = self.getContract(contractId)

        return (highway == contract)
