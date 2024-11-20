class EppReadyUploadDocsStepViewTests(ConstraforTestCase):
    def test_patch(self):
        self.force_authenticate_with_membership(self.contractor1_admin1)
        data = self.sample_data

        # step 1 - create and check objects created
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        epp_ready_flow_obj = EppReadyFlow.objects.filter(company=self.contractor1.company_ptr).first()
        invoice = epp_ready_flow_obj.invoice
        self.assertTrue(Invoice.objects.filter(id=invoice.id).exists())
        self.assertEqual(invoice.number, data["invoice_number"])
        self.assertEqual(invoice.project_id, data["project"])
        self.assertEqual(self.project.id, invoice.project_id)

        company_prequal_section = self.contractor1.company_ptr.prequal_section
        self.assertEqual(set(company_prequal_section.work_in_progress.all()), set(self.work_in_progress_list))

        fin_doc_filters_list = []
        passed_to_service_data = set_previous_and_current_year_in_bank_statements_by_current_date(self.sample_data)
        for fin_doc_request_data in passed_to_service_data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"] or FinancialDocument.UNDEFINED_PERIOD,
                "financial_quarter": fin_doc_request_data["financial_quarter"] or FinancialDocument.UNDEFINED_PERIOD,
                "financial_month": fin_doc_request_data["financial_month"] or FinancialDocument.UNDEFINED_PERIOD,
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        # 2 patch documents
        # 2.1. patch invoice data
        invoice_data = {
            "invoice_number": fake.lexify(),
            "invoice_amount": fake.random_int(1, 1000000),
            "invoice_uuid": invoice.id,
        }
        response = self.client.patch(self.url, invoice_data, format="json")

        invoice.refresh_from_db()
        self.assertEqual(invoice.id, response.data["invoice_uuid"])
        self.assertEqual(invoice.project.id, response.data["project"])
        self.assertEqual(invoice.amount, response.data["invoice_amount"])
        self.assertEqual(invoice.amount, invoice_data["invoice_amount"])
        self.assertEqual(invoice.number, response.data["invoice_number"])
        self.assertEqual(invoice.number, invoice_data["invoice_number"])

        company_prequal_section = self.contractor1.company_ptr.prequal_section
        self.assertEqual(set(company_prequal_section.work_in_progress.all()), set(self.work_in_progress_list))
        self.assertEqual(set(wip.uuid for wip in self.work_in_progress_list), set(response.data["work_in_progress"]))

        fin_doc_filters_list = []
        for fin_doc_request_data in response.data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"],
                "financial_quarter": fin_doc_request_data["financial_quarter"],
                "financial_month": fin_doc_request_data["financial_month"],
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        # 2.2. patch prequal data
        new_work_in_progress_list = [baker.make("file_manager.File") for _ in range(2)]
        prequal_data = {
            "work_in_progress": [file.uuid for file in new_work_in_progress_list],
        }
        response = self.client.patch(self.url, prequal_data, format="json")

        self.assertEqual(invoice.id, response.data["invoice_uuid"])
        self.assertEqual(invoice.project.id, response.data["project"])
        self.assertEqual(invoice.amount, response.data["invoice_amount"])
        self.assertEqual(invoice.number, response.data["invoice_number"])

        company_prequal_section = self.contractor1.company_ptr.prequal_section
        self.assertEqual(set(company_prequal_section.work_in_progress.all()), set(new_work_in_progress_list))
        self.assertEqual(set(wip.uuid for wip in new_work_in_progress_list), set(prequal_data["work_in_progress"]))
        self.assertEqual(set(wip.uuid for wip in new_work_in_progress_list), set(response.data["work_in_progress"]))

        fin_doc_filters_list = []
        for fin_doc_request_data in response.data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"],
                "financial_quarter": fin_doc_request_data["financial_quarter"],
                "financial_month": fin_doc_request_data["financial_month"],
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        # 2.3. patch prequal data
        new_w9_list = [baker.make("file_manager.File") for _ in range(3)]
        profile_data = {
            "w9_form": [file.uuid for file in new_w9_list],
        }
        response = self.client.patch(self.url, profile_data, format="json")

        self.assertEqual(invoice.id, response.data["invoice_uuid"])
        self.assertEqual(invoice.project.id, response.data["project"])
        self.assertEqual(invoice.amount, response.data["invoice_amount"])
        self.assertEqual(invoice.number, response.data["invoice_number"])

        self.assertEqual(
            set(file.uuid for file in company_prequal_section.work_in_progress.all()),
            set(response.data["work_in_progress"]),
        )

        self.assertEqual(
            set(file.uuid for file in self.contractor1.company_ptr.w9_form.all()), set(response.data["w9_form"])
        )
        self.assertEqual(
            set(file.uuid for file in self.contractor1.company_ptr.w9_form.all()), set(profile_data["w9_form"])
        )

        fin_doc_filters_list = []
        for fin_doc_request_data in response.data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"],
                "financial_quarter": fin_doc_request_data["financial_quarter"],
                "financial_month": fin_doc_request_data["financial_month"],
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        # 2.4. patch financial documents data
        # 2.4.1. add new balance sheet
        new_balance_sheet = baker.make("file_manager.File")
        new_balance_year = self.financial_year - 1
        balance_sheet_data = {
            "financial_documents": [
                {
                    "document_type": "balance_sheet",
                    "file": new_balance_sheet.uuid,
                    "financial_year": new_balance_year,
                    "financial_quarter": None,
                    "financial_month": None,
                },
            ],
        }
        response = self.client.patch(self.url, balance_sheet_data, format="json")

        self.assertEqual(invoice.id, response.data["invoice_uuid"])
        self.assertEqual(invoice.project.id, response.data["project"])
        self.assertEqual(invoice.amount, response.data["invoice_amount"])
        self.assertEqual(invoice.number, response.data["invoice_number"])

        self.assertEqual(
            set(file.uuid for file in company_prequal_section.work_in_progress.all()),
            set(response.data["work_in_progress"]),
        )

        self.assertEqual(
            set(file.uuid for file in self.contractor1.company_ptr.w9_form.all()), set(response.data["w9_form"])
        )

        fin_doc_filters_list = []
        for fin_doc_request_data in response.data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"],
                "financial_quarter": fin_doc_request_data["financial_quarter"],
                "financial_month": fin_doc_request_data["financial_month"],
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        balance_sheets = financial_documents.filter(document_type="balance_sheet")
        self.assertEqual(balance_sheets.count(), 2)  # 2024 and 2023
        self.assertEqual(balance_sheets.filter(financial_year=new_balance_year).first().file, new_balance_sheet)

        # 2.4.2. change existing balance sheet
        new_balance_year = self.financial_year - 2
        balance_sheet_data = {
            "financial_documents": [
                {
                    "document_type": "balance_sheet",
                    "file": new_balance_sheet.uuid,
                    "financial_year": new_balance_year,
                    "financial_quarter": None,
                    "financial_month": None,
                },
            ],
        }
        response = self.client.patch(self.url, balance_sheet_data, format="json")

        self.assertEqual(invoice.id, response.data["invoice_uuid"])
        self.assertEqual(invoice.project.id, response.data["project"])
        self.assertEqual(invoice.amount, response.data["invoice_amount"])
        self.assertEqual(invoice.number, response.data["invoice_number"])

        self.assertEqual(
            set(file.uuid for file in company_prequal_section.work_in_progress.all()),
            set(response.data["work_in_progress"]),
        )

        self.assertEqual(
            set(file.uuid for file in self.contractor1.company_ptr.w9_form.all()), set(response.data["w9_form"])
        )

        fin_doc_filters_list = []
        for fin_doc_request_data in response.data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"],
                "financial_quarter": fin_doc_request_data["financial_quarter"],
                "financial_month": fin_doc_request_data["financial_month"],
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        balance_sheets = financial_documents.filter(document_type="balance_sheet")
        self.assertEqual(balance_sheets.count(), 2)  # 2024 and 2022
        self.assertEqual(balance_sheets.filter(financial_year=new_balance_year).first().file, new_balance_sheet)

        # 2.4.3. chnge existing bank statement file
        new_bank_statement = baker.make("file_manager.File")
        bank_statement_data = {
            "financial_documents": [
                {
                    "document_type": "bank_statement",
                    "file": new_bank_statement.uuid,
                    "financial_year": None,
                    "financial_quarter": None,
                    "financial_month": self.current_date_minus_1_month.month,
                },
            ],
        }
        response = self.client.patch(self.url, bank_statement_data, format="json")

        self.assertEqual(invoice.id, response.data["invoice_uuid"])
        self.assertEqual(invoice.project.id, response.data["project"])
        self.assertEqual(invoice.amount, response.data["invoice_amount"])
        self.assertEqual(invoice.number, response.data["invoice_number"])

        self.assertEqual(
            set(file.uuid for file in company_prequal_section.work_in_progress.all()),
            set(response.data["work_in_progress"]),
        )

        self.assertEqual(
            set(file.uuid for file in self.contractor1.company_ptr.w9_form.all()), set(response.data["w9_form"])
        )

        fin_doc_filters_list = []
        for fin_doc_request_data in response.data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"],
                "financial_quarter": fin_doc_request_data["financial_quarter"],
                "financial_month": fin_doc_request_data["financial_month"],
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        bank_statement = financial_documents.filter(document_type="bank_statement")
        self.assertEqual(bank_statement.count(), 3)  # 3 last months
        self.assertTrue(bank_statement.filter(file=new_bank_statement).exists())

        # 2.4.4. add new bank statement and change existing one
        new_bank_statement_1 = baker.make("file_manager.File")
        new_bank_statement_2 = baker.make("file_manager.File")
        new_bank_statement_1_month = self.current_date_minus_3_month - relativedelta(months=1)
        bank_statement_data = {
            "financial_documents": [
                {
                    "document_type": "bank_statement",
                    "file": new_bank_statement_1.uuid,
                    "financial_year": None,
                    "financial_quarter": None,
                    "financial_month": new_bank_statement_1_month.month,
                },
                {
                    "document_type": "bank_statement",
                    "file": new_bank_statement_2.uuid,
                    "financial_year": None,
                    "financial_quarter": None,
                    "financial_month": self.current_date_minus_2_month.month,
                },
            ],
        }
        response = self.client.patch(self.url, bank_statement_data, format="json")

        self.assertEqual(invoice.id, response.data["invoice_uuid"])
        self.assertEqual(invoice.project.id, response.data["project"])
        self.assertEqual(invoice.amount, response.data["invoice_amount"])
        self.assertEqual(invoice.number, response.data["invoice_number"])

        self.assertEqual(
            set(file.uuid for file in company_prequal_section.work_in_progress.all()),
            set(response.data["work_in_progress"]),
        )

        self.assertEqual(
            set(file.uuid for file in self.contractor1.company_ptr.w9_form.all()), set(response.data["w9_form"])
        )

        fin_doc_filters_list = []
        for fin_doc_request_data in response.data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"],
                "financial_quarter": fin_doc_request_data["financial_quarter"],
                "financial_month": fin_doc_request_data["financial_month"],
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        bank_statement = financial_documents.filter(document_type="bank_statement")
        self.assertEqual(bank_statement.count(), 4)  # 3 last months + new bank statement
        self.assertTrue(bank_statement.filter(file=new_bank_statement_1).exists())
        self.assertTrue(bank_statement.filter(file=new_bank_statement_2).exists())

        # 2.4.5. add new income statement and change existing one
        new_income_statement = baker.make("file_manager.File")
        new_income_statement_year = self.financial_year - 1
        income_statement_data = {
            "financial_documents": [
                {
                    "document_type": "income_statement",
                    "file": self.income_statement_2024.uuid,
                    "financial_year": new_income_statement_year,
                    "financial_quarter": None,
                    "financial_month": None,
                },
                {
                    "document_type": "income_statement",
                    "file": new_income_statement.uuid,
                    "financial_year": self.financial_year,
                    "financial_quarter": None,
                    "financial_month": None,
                },
            ],
        }
        response = self.client.patch(self.url, income_statement_data, format="json")

        self.assertEqual(invoice.id, response.data["invoice_uuid"])
        self.assertEqual(invoice.project.id, response.data["project"])
        self.assertEqual(invoice.amount, response.data["invoice_amount"])
        self.assertEqual(invoice.number, response.data["invoice_number"])

        self.assertEqual(
            set(file.uuid for file in company_prequal_section.work_in_progress.all()),
            set(response.data["work_in_progress"]),
        )

        self.assertEqual(
            set(file.uuid for file in self.contractor1.company_ptr.w9_form.all()), set(response.data["w9_form"])
        )

        fin_doc_filters_list = []
        for fin_doc_request_data in response.data["financial_documents"]:
            fin_doc_filters = {
                "document_type": fin_doc_request_data["document_type"],
                "file__uuid": fin_doc_request_data["file"],
                "financial_year": fin_doc_request_data["financial_year"],
                "financial_quarter": fin_doc_request_data["financial_quarter"],
                "financial_month": fin_doc_request_data["financial_month"],
            }
            fin_doc_filters_list.append(fin_doc_filters)

        epp_subcontractor = self.contractor1.company_ptr.epp_subcontractor_maps.first()
        financial_documents = epp_subcontractor.financial_documents.all()

        for filter_set in fin_doc_filters_list:
            self.assertTrue(financial_documents.filter(**filter_set).exists())

        income_statement = financial_documents.filter(document_type="income_statement")
        self.assertEqual(income_statement.count(), 2)
        self.assertTrue(income_statement.filter(file=new_income_statement).exists())
