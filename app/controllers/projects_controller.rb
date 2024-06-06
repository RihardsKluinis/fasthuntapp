class ProjectsController < ApplicationController
  before_action :set_project, only: %i[ show edit update destroy ]
  protect_from_forgery except: [:index]

  # GET /projects or /projects.json
  def index
    @projects = ProjectLaunch.order('RANDOM()').paginate(page: params[:page], per_page: 20)
    respond_to do |format|
      format.html
      format.js
    end
  end

  def show
    @project = ProjectLaunch.find(params[:id])
    @profiles = @project.profiles
  end

  # GET /projects/new
  def new
    @project = ProjectLaunch.new
  end

  # GET /projects/1/edit
  def edit
  end

  # POST /projects or /projects.json
  def create
    @project = ProjectLaunch.new(project_params)

    respond_to do |format|
      if @project.save
        format.html { redirect_to project_url(@project), notice: "Project launch was successfully created." }
        format.json { render :show, status: :created, location: @project }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @project.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /projects/1 or /projects/1.json
  def update
    respond_to do |format|
      if @project.update(project_params)
        format.html { redirect_to project_url(@project), notice: "Project launch was successfully updated." }
        format.json { render :show, status: :ok, location: @project }
      else
        format.html { render :edit, status: :unprocessable_entity }
        format.json { render json: @project.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /projects/1 or /projects/1.json
  def destroy
    @project.destroy!

    respond_to do |format|
      format.html { redirect_to projects_url, notice: "Project launch was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_project
    @project = ProjectLaunch.find(params[:id])
  end

  # Only allow a list of trusted parameters through.
  def project_params
    params.require(:project).permit(:name, :description, :date, :image, :website, :project_id)
  end
end
